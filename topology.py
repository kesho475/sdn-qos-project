from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
import os

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
    
    print("\n*** Configuring Hardware QoS Queues on Switch 1 ***")
    # Queue 0 (Slow Lane): Max 2 Mbps
    # Queue 1 (VIP Lane): Min 8 Mbps, Max 10 Mbps
    os.system("ovs-vsctl -- set Port s1-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=10000000 queues=0=@q0,1=@q1 -- --id=@q0 create Queue other-config:max-rate=2000000 -- --id=@q1 create Queue other-config:min-rate=8000000 other-config:max-rate=10000000 > /dev/null 2>&1")
    os.system("ovs-vsctl -- set Port s1-eth2 qos=@newqos2 -- --id=@newqos2 create QoS type=linux-htb other-config:max-rate=10000000 queues=0=@q0,1=@q1 -- --id=@q0 create Queue other-config:max-rate=2000000 -- --id=@q1 create Queue other-config:min-rate=8000000 other-config:max-rate=10000000 > /dev/null 2>&1")
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()
