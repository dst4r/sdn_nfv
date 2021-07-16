from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController

# hosts connections
# h0 h0-eth0:es0-eth1
# h1 h1-eth0:es0-eth2
# h2 h2-eth0:es1-eth1
# h3 h3-eth0:es1-eth2
# h4 h4-eth0:es2-eth1
# h5 h5-eth0:es2-eth2
# h6 h6-eth0:es3-eth1
# h7 h7-eth0:es3-eth2
# h8 h8-eth0:es4-eth1
# h9 h9-eth0:es4-eth2
# h10 h10-eth0:es5-eth1
# h11 h11-eth0:es5-eth2
# h12 h12-eth0:es6-eth1
# h13 h13-eth0:es6-eth2
# h14 h14-eth0:es7-eth1
# h15 h15-eth0:es7-eth2

REMOTE_CONTROLLER_IP = "127.0.0.1"


def testing():
    topo = MyTopo()
    net = Mininet(topo=topo, link=TCLink, controller=RemoteController)
    net.addController("c0",
                      controller=RemoteController,
                      ip=REMOTE_CONTROLLER_IP,
                      port=6633)
    net.start()
    
    print "=== Dumping hosts connections ==="
    dumpNodeConnections(net.hosts)
    
    print "=== Testing network connectivity ==="
    net.pingAll()

    print "=== Testing bandwidth between h1 as a client and h12, h0 as servers ==="
    # Iperf servers hosts h0 in pod0 and h12 in pod3
    h0, h12 = net.get('h0', 'h12')
    # Iperf client hosts h1 in pod0
    h1 = net.get('h1')

    # Iperf servers h0, h12 running in background
    h0.popen('iperf -s -u -i 1', shell=True)
    h12.popen('iperf -s -u -i 1', shell=True)

    # Iperf client h1 print the results
    h1.cmdPrint('iperf -c '+ h0.IP() + ' -u -t 10 -i 1 -b 100m')
    h1.cmdPrint('iperf -c '+ h12.IP() + ' -u -t 10 -i 1 -b 100m')

    CLI(net)
    net.stop()


class MyTopo(Topo):
    def __init__(self):

        # Initialize topology
        Topo.__init__(self)

        # Add 16 hosts
        hosts = [self.addHost('h%d' % i) for i in range(0, 16)]

        # Add 4 core switches
        core_switches = [self.addSwitch('cs%d' % i) for i in range(0, 4)]

        # Add 8 aggregation switches
        aggregation_switches = [self.addSwitch('as%d' % i) for i in range(0, 8)]

        # Add 8 edge switches
        edge_switches = [self.addSwitch('es%d' % i) for i in range(0, 8)]

        # Add links between edge switches and hosts
        for i in range(0, 16):
            if i % 2 == 0:
                es_index = i/2
            self.addLink(hosts[i], edge_switches[es_index])

        # Add links between edge switches and aggregation switches
        for i in range(0, 8):
            # one to one mapping
            self.addLink(aggregation_switches[i], edge_switches[i])

            # cross links between edge switches and aggregation switches
            if i % 2 == 0:
                self.addLink(aggregation_switches[i],
                             edge_switches[i+1])
            else:
                self.addLink(aggregation_switches[i],
                             edge_switches[i-1])

        # Add links between core switches and aggregation switches
        for i in range(0, 8):
            if i % 2 == 0:
                self.addLink(core_switches[0],
                             aggregation_switches[i])
                self.addLink(core_switches[1],
                             aggregation_switches[i])
            else:
                self.addLink(core_switches[2],
                             aggregation_switches[i])
                self.addLink(core_switches[3],
                             aggregation_switches[i])


topos = {'mytopo': (lambda: MyTopo())}

if __name__ == '__main__':
    setLogLevel('info')
    testing()
