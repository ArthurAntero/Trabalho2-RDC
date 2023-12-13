from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def topologia():
    net = Mininet(controller=Controller, switch=OVSSwitch, link=TCLink)

    # Adicionar um controlador padrão
    c0 = net.addController('c0')

    # Adicionar switch(comutador)
    s1 = net.addSwitch('s1')

    # Adicionar hosts
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')
    h4 = net.addHost('h4', ip='10.0.0.4')

    # Adicionar links
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)

    # Iniciar a rede
    net.build()
    c0.start()
    s1.start([c0])

    # Executar o CLI do Mininet
    CLI(net)

    # Parar a rede
    net.stop()

if __name__ == '_main_':
    setLogLevel('info')
    topologia()
