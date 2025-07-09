# Guia de Instalação e Execução do Ambiente Mininet e Ryu no Windows

Este guia detalha o processo de configuração de uma máquina virtual Linux no Windows para hospedar o ambiente Mininet e o controlador Ryu.

**Plataforma Host:** Windows 10/11
**Plataforma Convidada (VM):** Ubuntu Server 22.04 LTS (recomendado pela leveza) ou Ubuntu Desktop 22.04 LTS (se preferir interface gráfica)

## 1. Pré-requisitos para o Windows

Antes de começar, baixe os seguintes softwares no seu sistema Windows:

1.  **Oracle VM VirtualBox:**
    * Faça o download do instalador para Windows hosts em: [https://www.virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads)
    * **Importante:** Baixe também o **VirtualBox 7.0.x Oracle VM VirtualBox Extension Pack** (o número da versão deve corresponder à sua versão da VirtualBox).

2.  **Imagem ISO do Ubuntu Server ou Desktop:**
    * **Ubuntu Server 22.04 LTS:** [https://ubuntu.com/download/server](https://ubuntu.com/download/server) (Recomendado para melhor desempenho em VM)
    * **Ubuntu Desktop 22.04 LTS:** [https://ubuntu.com/download/desktop](https://ubuntu.com/download/desktop)

## 2. Instalação da Oracle VM VirtualBox no Windows

1.  **Execute o Instalador da VirtualBox:**
    * Localize o arquivo `VirtualBox-X.X.X-XXXXX-Win.exe` que você baixou e clique duas vezes nele.
    * Siga as instruções do assistente de instalação. Geralmente, as opções padrão são suficientes. Clique em "Next", "Next", "Yes", "Install".
    * Durante a instalação, pode ser que sua conexão de rede seja temporariamente desativada. Isso é normal.
    * Ao final, desmarque a opção "Start Oracle VM VirtualBox after installation" por enquanto e clique em "Finish".

2.  **Instale o VirtualBox Extension Pack:**
    * Localize o arquivo `Oracle_VM_VirtualBox_Extension_Pack-X.X.X.vbox-extpack` que você baixou.
    * Clique duas vezes nele. A VirtualBox será aberta e perguntará se você deseja instalá-lo.
    * Clique em "Instalar" ou "Install" e aceite os termos de licença. Isso adiciona funcionalidades como suporte a USB 2.0/3.0, RDP, e boot PXE.

## 3. Criação e Configuração da Máquina Virtual Ubuntu

1.  **Abra a VirtualBox:**
    * No Windows, procure por "Oracle VM VirtualBox" e abra o aplicativo.

2.  **Crie uma Nova Máquina Virtual:**
    * Clique em "Nova" (ou "New") no menu superior.
    * **Nome:** `UbuntuSDN` (ou um nome de sua escolha)
    * **Pasta da Máquina:** Deixe o padrão ou escolha um local com bastante espaço.
    * **Imagem ISO:** Clique na seta para baixo e depois em "Outro..." (ou "Other...") e selecione o arquivo ISO do Ubuntu que você baixou.
    * **Pular Instalação Desassistida:** Marque a caixa "Pular Instalação Desassistida" (ou "Skip Unattended Installation") se estiver usando Ubuntu Server, pois o instalador manual é preferível para iniciantes. Se for Desktop, pode deixar desmarcado.
    * Clique em "Próximo" (ou "Next").

3.  **Configurar Hardware (RAM e CPUs):**
    * **Memória RAM:** Recomendo pelo menos `4096 MB` (4 GB) para um bom desempenho. Ajuste de acordo com a RAM disponível no seu Windows.
    * **Processadores (CPUs):** Recomendo pelo menos `2` CPUs. Ajuste de acordo com o número de núcleos do seu processador.
    * Clique em "Próximo".

4.  **Configurar Disco Rígido Virtual:**
    * **Tamanho do Disco:** Recomendo pelo menos `25 GB`.
    * Mantenha "Criar um novo disco rígido virtual agora" selecionado.
    * Clique em "Próximo".

5.  **Revisar e Finalizar:**
    * Revise as configurações. Se estiver tudo certo, clique em "Finalizar" (ou "Finish").

6.  **Configurações de Rede da VM (Importante!):**
    * Com a VM `UbuntuSDN` selecionada na lista da VirtualBox, clique em "Configurações" (ou "Settings").
    * Vá para "Rede" (ou "Network").
    * **Adaptador 1:**
        * **Anexado a:** Mude de "NAT" para **"Adaptador em Ponte"** (ou "Bridged Adapter").
        * **Nome:** Selecione a sua placa de rede física do Windows (ex: "Intel(R) Ethernet Connection", "Realtek PCIe GbE Family Controller", "Wi-Fi").
        * Isso fará com que sua VM receba um IP na mesma rede que seu computador Windows, facilitando a comunicação.
    * Clique em "OK".

## 4. Instalação do Ubuntu Server/Desktop na Máquina Virtual

1.  **Inicie a Máquina Virtual:**
    * Selecione a VM `UbuntuSDN` na VirtualBox e clique em "Iniciar" (ou "Start").

2.  **Siga o Processo de Instalação do Ubuntu:**
    * **Idioma:** Escolha seu idioma.
    * **Layout do Teclado:** Selecione o layout correto (ex: `Português (Brasil)`).
    * **Tipo de Instalação:**
        * Para **Ubuntu Server**: Escolha "Ubuntu Server" e siga as instruções. Configure o usuário/senha.
        * Para **Ubuntu Desktop**: Escolha "Instalação normal" e siga as instruções. Configure o usuário/senha.
    * **Particionamento:** Escolha "Usar disco inteiro" ou "Apagar disco e instalar Ubuntu". Como é uma VM nova, não há problema em usar o disco inteiro da VM.
    * Aguarde a instalação. Ao final, ele pedirá para "Reiniciar Agora". Pressione Enter e a VM reiniciará. Pode ser que você precise "ejetar" a ISO virtualmente (Dispositivos > Unidades Ópticas > Remover disco da unidade virtual) antes de reiniciar completamente para não iniciar o instalador novamente.

3.  **Login na VM:**
    * Após reiniciar, faça login com o usuário e senha que você configurou durante a instalação.

4.  **Atualizar o Sistema da VM:**
    Dentro da VM Ubuntu, execute os comandos para atualizar o sistema:

    ```bash
    sudo apt update
    sudo apt upgrade -y
    ```

5.  **Instalar o OpenSSH Server (Recomendado):**
    Isso permitirá que você acesse a VM via SSH a partir do seu Windows (usando Putty, Terminal, etc.), o que é mais conveniente do que a interface da VirtualBox.

    ```bash
    sudo apt install openssh-server -y
    ```
    Para encontrar o IP da sua VM no Ubuntu:
    ```bash
    ip a
    ```
    Procure por `inet` sob a sua interface de rede (geralmente `enp0s3` ou similar).

## 5. Instalação do Mininet e Ryu na Máquina Virtual Ubuntu

Agora que você tem um Ubuntu funcionando na sua VM, os passos são os mesmos que seriam em qualquer máquina Linux.

### 5.1. Instalação do Mininet

1.  **Atualizar o Sistema (dentro da VM Ubuntu):**
    ```bash
    sudo apt update
    sudo apt upgrade -y
    ```

2.  **Clonar o Repositório do Mininet (dentro da VM Ubuntu):**
    ```bash
    git clone [https://github.com/mininet/mininet](https://github.com/mininet/mininet)
    ```

3.  **Acessar o Diretório e Executar o Script de Instalação (dentro da VM Ubuntu):**
    ```bash
    cd mininet
    mininet/util/install.sh -a
    ```
    *Este processo pode levar algum tempo.*

4.  **Verificar a Instalação (dentro da VM Ubuntu):**
    ```bash
    sudo mn --test pingall
    ```
    Você deverá ver uma mensagem de sucesso. Para sair, digite `exit`.

### 5.2. Instalação do Ryu Controller (dentro da VM Ubuntu)

1.  **Instalar Pip (se não tiver):**
    ```bash
    sudo apt install python3-pip -y
    ```

2.  **Instalar o Ryu:**
    ```bash
    pip install ryu
    ```

3.  **Verificar a Instalação do Ryu:**
    ```bash
    python3 -c "import ryu"
    ```
    Se não houver mensagens de erro, a instalação foi bem-sucedida.

## 6. Configuração do Repositório do Projeto na VM

1.  **Clonar seu Repositório (dentro da VM Ubuntu):**
    Navegue até o diretório onde você deseja armazenar seu projeto (ex: `cd ~` para seu diretório home) e clone o repositório.

    ```bash
    git clone [https://github.com/seu-usuario/sdn-ryu-load-balancer.git](https://github.com/seu-usuario/sdn-ryu-load-balancer.git)
    cd sdn-ryu-load-balancer
    ```
    *Lembre-se de substituir `https://github.com/seu-usuario/sdn-ryu-load-balancer.git` pelo URL real do seu repositório.*

## 7. Executando o Ambiente

Para rodar o projeto, você precisará de dois terminais abertos **dentro da sua Máquina Virtual Ubuntu**. Se você instalou o SSH Server (Passo 4.5), pode abrir dois terminais SSH do seu Windows para a VM, o que é mais prático. Caso contrário, abra dois terminais diretamente na interface gráfica da VM (se for Desktop) ou use multiplexadores como `tmux` ou `screen` (se for Server).

### Passo 1: Iniciar o Controlador Ryu

1.  No **primeiro terminal da VM Ubuntu**.
2.  Navegue até o diretório raiz do seu projeto (onde você clonou `sdn-ryu-load-balancer`).
3.  Execute o controlador Ryu.

    ```bash
    ryu-manager code/ryu_controller/sdn_load_balancer.py
    ```
    Você deverá ver logs do Ryu começando, indicando que o controlador está ativo e aguardando conexões de switches.

### Passo 2: Iniciar a Topologia Mininet

1.  No **segundo terminal da VM Ubuntu**.
2.  Navegue até o diretório raiz do seu projeto.
3.  Execute o script da topologia Mininet. Este script criará a rede virtual e a conectará ao seu controlador Ryu (que está rodando no primeiro terminal).

    ```bash
    sudo python3 examples/mininet_topology.py
    ```
    *Nota: `sudo` é necessário para rodar o Mininet.*

    Após a execução, você verá o prompt do Mininet (`mininet>`), indicando que a rede está ativa.

### Passo 3: Testar a Rede e o Controlador

Com o Mininet CLI (no segundo terminal da VM) e o Ryu Controller (no primeiro terminal da VM) rodando, você pode começar a testar:

1.  **Testar Conectividade:**
    No terminal do Mininet, ping de um host para outro para ver se a rede funciona. O controlador Ryu deverá instalar as regras de fluxo.

    ```mininet>
    pingall
    ```
    Ou teste pings específicos:

    ```mininet>
    h1 ping -c 3 h4
    ```

2.  **Gerar Tráfego para Balanceamento de Carga:**
    Para observar o balanceamento de carga e o monitoramento, você pode gerar tráfego usando `iperf`.

    * No terminal do Mininet, inicie um servidor `iperf` em um host:

        ```mininet>
        h1 iperf -s &
        ```
    * Em outro host, inicie um cliente `iperf` para gerar tráfego para `h1`:

        ```mininet>
        h4 iperf -c h1
        ```
    * Observe os logs no terminal do Ryu (primeiro terminal da VM). Você deverá ver as estatísticas das portas sendo coletadas e, se o limite de ocupação for atingido, mensagens sobre o redirecionamento de tráfego pelo balanceador de carga.

3.  **Visualizar Informações do Mininet:**
    No terminal do Mininet, você pode usar comandos como:

    ```mininet>
    nodes # Lista todos os nós (hosts e switches)
    links # Lista todos os links
    net   # Mostra uma visão geral da rede
    dump  # Exibe informações detalhadas dos nós
    ```

### Passo 4: Parar o Ambiente

1.  **Sair do Mininet:**
    No terminal do Mininet, digite `exit`.

    ```mininet>
    exit
    ```
    Isso irá parar a rede simulada e remover os processos do Mininet.

2.  **Parar o Controlador Ryu:**
    No terminal onde o Ryu está rodando, pressione `Ctrl+C`.

    ```bash
    ^C
    ```

Este guia passo a passo deve ser suficiente para configurar e executar seu ambiente de testes no Windows via VirtualBox. Em caso de dúvidas ou problemas, consulte a documentação oficial do Mininet, Ryu e VirtualBox.
