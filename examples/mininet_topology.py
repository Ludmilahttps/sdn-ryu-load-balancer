from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def simple_topology():
    "Cria e testa uma topologia simples com 3 switches e 4 hosts."

    # Inicia o log em info para ver mensagens do Mininet
    setLogLevel('info')

    # Cria uma instância de Mininet com um controlador remoto
    # OIP padrão é 127.0.0.1, porta padrão é 6653
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)

    info('*** Adicionando controlador\n')
    # Assumindo que o controlador Ryu está rodando em localhost na porta 6653
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

    info('*** Adicionando hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    h4 = net.addHost('h4', ip='10.0.0.4/24')

    info('*** Adicionando switches\n')
    s1 = net.addSwitch('s1', protocols='OpenFlow13') # Especifica o protocolo OpenFlow 1.3
    s2 = net.addSwitch('s2', protocols='OpenFlow13')
    s3 = net.addSwitch('s3', protocols='OpenFlow13')

    info('*** Criando links\n')
    # Links entre hosts e switches
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s3)

    # Links entre switches (para múltiplos caminhos e balanceamento de carga)
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s2, s3) # Pode-se adicionar mais links para uma topologia em malha mais complexa

    info('*** Iniciando rede\n')
    net.start()

    info('*** Testando conectividade inicial\n')
    # Um teste de ping entre todos os hosts pode ser feito aqui,
    # mas o controlador Ryu precisa instalar as regras primeiro
    # net.pingAll() # Pode falhar se o controlador ainda não estiver pronto

    info('*** Executando CLI\n')
    CLI(net) # Abre a interface de linha de comando do Mininet

    info('*** Parando rede\n')
    net.stop()

if __name__ == '__main__':
    simple_topology()
