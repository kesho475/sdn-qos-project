from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI

class QoSTopo(Topo):
    def build(self):
        h1 = self.addHost('h1', ip='10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.2')
        s1 = self.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13')
        self.addLink(h1, s1, cls=TCLink, bw=10, delay='5ms')
        self.addLink(h2, s1, cls=TCLink, bw=10, delay='5ms')

def run():
    topo = QoSTopo()
    net = Mininet(topo=topo, controller=RemoteController, link=TCLink)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()
