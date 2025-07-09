from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet
from ryu.lib import hub

class SimpleLoadBalancer(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    
    def __init__(self, *args, **kwargs):
        super(SimpleLoadBalancer, self).__init__(*args, **kwargs)
        self.mac_to_port = {}  # dpid -> {mac: port}
        self.datapaths = {}
        self.port_stats = {}   # dpid -> {port_no: tx_packets}
        self.round_robin_index = {}  # dpid -> int
        self.monitor_thread = hub.spawn(self._monitor)

    # Enviar solicitação de estatísticas a cada 5 segundos
    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(5)

    def _request_stats(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        dpid = ev.msg.datapath.id
        self.port_stats.setdefault(dpid, {})
        for stat in ev.msg.body:
            self.port_stats[dpid][stat.port_no] = stat.tx_packets
        self.logger.info("Port stats (dpid %s): %s", dpid, self.port_stats[dpid])

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Instalar regra default para enviar pacotes desconhecidos ao controlador
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        self.datapaths[datapath.id] = datapath
        self.round_robin_index[datapath.id] = 0

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        if buffer_id is not None:
            mod = parser.OFPFlowMod(
                datapath=datapath,
                buffer_id=buffer_id,
                priority=priority,
                match=match,
                instructions=inst
            )
        else:
            mod = parser.OFPFlowMod(
                datapath=datapath,
                priority=priority,
                match=match,
                instructions=inst
            )

        datapath.send_msg(mod)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid = datapath.id

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        if eth.ethertype == 0x88cc:  # Ignorar LLDP
            return

        dst = eth.dst
        src = eth.src
        in_port = msg.match['in_port']

        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src] = in_port

        # Se o destino já é conhecido, usamos a porta correspondente
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
            self.logger.info(f"Destino {dst} conhecido, enviando para porta {out_port}")
        else:
            ports = self.port_stats.get(dpid)
            if ports:
                valid_ports = [p for p in ports.keys() if p != ofproto.OFPP_LOCAL and p != in_port]
                if valid_ports:
                    sorted_ports = sorted(valid_ports, key=lambda p: ports[p])
                    min_val = ports[sorted_ports[0]]
                    tied_ports = [p for p in sorted_ports if ports[p] == min_val]
                    idx = self.round_robin_index[dpid] % len(tied_ports)
                    out_port = tied_ports[idx]
                    self.round_robin_index[dpid] += 1
                    self.logger.info(f"Destino {dst} desconhecido. Balanceando: escolhida porta {out_port}")
                else:
                    out_port = ofproto.OFPP_FLOOD
                    self.logger.info(f"Nenhuma porta válida encontrada. Flood para {dst}")
            else:
                out_port = ofproto.OFPP_FLOOD
                self.logger.info(f"Nenhuma estatística disponível. Flood para {dst}")

        actions = [parser.OFPActionOutput(out_port)]

        # Instala a regra de fluxo
        match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
        if msg.buffer_id != ofproto.OFP_NO_BUFFER:
            self.add_flow(datapath, 1, match, actions, msg.buffer_id)
            return
        else:
            self.add_flow(datapath, 1, match, actions)

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=msg.data
        )
        datapath.send_msg(out)
