# SDN Ryu Load Balancer

Ludmila Silveira - 22102068
Fernando Moretti - 
Lucas -
Pedro -

Este projeto implementa um controlador SDN (Software-Defined Networking) utilizando o framework Ryu, focado em aprendizado de endereços MAC (switch L2), monitoramento de portas de switches e balanceamento de carga dinâmico. O objetivo principal é demonstrar as vantagens da arquitetura SDN na gestão eficiente do tráfego de rede, evitando congestionamentos e otimizando o uso de links.

## 1. Objetivos do Projeto

O Plano de Controle implementado visa:

* **Implementar um controlador SDN** utilizando o framework Ryu.
* Realizar o **aprendizado de endereços MAC (switch L2)**.
* **Monitorar as portas dos switches** (quantidade de pacotes/bytes transmitidos).
* Implementar **balanceamento de carga dinâmico**, redirecionando tráfego com base na ocupação das portas.

## 2. Visão Geral dos Resultados

Os resultados esperados incluem a demonstração da capacidade do controlador em gerenciar fluxos de dados, responder a condições de congestionamento e distribuir eficientemente o tráfego na rede simulada no Mininet. Serão gerados logs informativos sobre a ocupação das portas e as decisões do controlador.

## 3. Estrutura da Rede Simulada

A rede será simulada no Mininet, com uma topologia em árvore ou malha, contendo:

* 3 switches (s1, s2, s3).
* 4 hosts (h1, h2, h3, h4).
* Vários caminhos entre origem e destino.

O controlador utilizado será o Ryu.

## 4. Algoritmos e Lógica do Plano de Controle

### 4.1. Switch Learning L2 (Aprendizado de Endereços MAC)

* Funciona como um switch Ethernet inteligente: quando um pacote chega, o controlador aprende o MAC de origem e usa esse conhecimento para encaminhar pacotes futuros.
* O controlador instalará dinamicamente regras de encaminhamento (flow_mod) nos switches.

### 4.2. Monitoramento de Tráfego das Portas

* O controlador consultará periodicamente os switches para saber quantos pacotes/bytes passaram por cada porta.
* Serão utilizadas mensagens `PortStatsRequest` e `PortStatsReply` do protocolo OpenFlow.

### 4.3. Balanceamento de Carga

* Define um limite de ocupação de porta.
* Quando o limite é excedido (porta muito carregada), o controlador irá redirecionar novos fluxos para outra porta com menos tráfego.
* A lógica de escolha será baseada em menor carga ou round-robin em caso de empate.
* A detecção de congestionamento e o redirecionamento automático de fluxos ativos serão funcionalidades chave.

## 5. APIs OpenFlow Utilizadas

* `PortStatsRequest / Reply`: Consulta de estatísticas de porta.
* `FlowMod`: Adição, modificação e remoção de regras de fluxo.
* `PacketIn / PacketOut`: Comunicação entre switches e o controlador.

## 6. Configuração e Execução do Ambiente

### 6.1. Pré-requisitos

Certifique-se de ter instalado:

* **Python 3**
* **Ryu**: Framework de controlador SDN.
* **Mininet**: Emulador de rede para criar a topologia.

### 6.2. Instalação de Dependências

```bash
# Instalar o Ryu (se ainda não tiver)
pip install ryu

# Instalar o Mininet (consulte a documentação oficial para a sua distribuição Linux)
# Exemplo para Ubuntu:
# git clone git://[github.com/mininet/mininet](https://github.com/mininet/mininet)
# mininet/util/install.sh -a
