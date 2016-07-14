#!/usr/bin/python
#Script Name: SingleTopoCustom.py
#Auther: Haiqi Jiang
#Created: 14th July 2016
#Last Modified:
#Desception
"""
This script create one network to connect one controller, 1 switch and 4 hosts.
Besides, the link between switch and host is defined by us in order to prefare 
for the follow-up work.
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink

class SingleSwitchTopo(Topo):
    def build(self, n = 2):
        controller = self.addController('c1')
        switch = self.addSwitch('s1')
        self.addLink(controller, switch)
        for h in range(n):
            host = slef.addHost('h%s' %(h+1), cpu = 0.5/n)
            #10 Mbps, 5ms delay, 10% loss, 1000 packet queue
            self.addLink(host, switch, bw = 10,
            delay = '5ms', loss = 10, max_queue_size = 1000, use_htb = True)
            
def simpleTest():
    topo = SingleSwitchTopo(n = 4)
    net = Mininet(topo = topo, host = CPULimitedHost, link = TCLink)
    net.start()
    print 'Dumping host connections'
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    print "testing bandwidth between h1 and h4"
    h1,h4 = net.get('h1', 'h4')
    net.iperf((h1, h4))
    net.stop()
    
    
if __name__ == "__main__":
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
