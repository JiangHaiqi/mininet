#coding= utf-8
#Script Name: multiLayerNetwoek.py
#Auther: Haiqi Jiang
#Created: 15th July 2016
#Last Modified:
#desception:

from mininet.cli import CLI
from mininet.log import setLoglevel, info
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch

def myTopo(key):
    net = Mininet(listenPort = 6634, autoSetMacs = True, ipBase = '10.0.0.0/8', autoStaticArp = False)
    info("***creating network****\n")
    info("***add controller***")
    mycontroller = RemoteController("floodlight", ip = "192.168.0.18", port = 6633)
    net.addController(mycontroller)
    info('***add core switches***\n')
    for i in range(1, key*key/4 + 1):
        switch_c = net.addSwitch('s%d%d' %(key+1, i))
        
    info('***add aggregation switch****')
    for i in range(1, key+1):
        for j in range(1, key/2 + 1):
            switch_au = net.addSwitch('s%d%d' %(i,j))
        for j in range(key/2 + 1, key +1):
            switch_ad = net.addSwitch('s%d%d' %(i,j))
    info('***add hosts***\n')
    for i in range(1, key*key*key/4+1):
        host = net.addHost("h%d" %i)
        
    info("***add link between core switches and aggregation switch***\n")
    for i in range(1, key*key/4+1):
        switch_c = net.get('s%d%d' %(key+1,i))
        for j in range(1, key+1):
            switch_au = net.get('s%d%d' %(j,(i-1)/(key/2)+1))
            net.addLink(switch_c,switch_au)
            
    info('****Add links between two layer aggregation switches****\n')
    
    for i in range( 1, key+1 ):
        for j in range( 1, key/2+1 ):
            switch_au = net.get( 's%d%d' %(i,j) )
            for k in range( key/2+1, key+1 ):
                switch_ad = net.get( 's%d%d' %(i,k) )
                net.addLink( switch_au, switch_ad )
    
    info('****Add links between aggregation switches and hosts****\n')
    
    for i in range( 1, key+1 ):
        for j in range( 1, key/2+1 ):
            switch_ad = net.get( 's%d%d' %(i,j+key/2) )
            for k in range( 1, key/2+1 ):
                host = net.get( 'h%d' %((i-1)*key*key/4+(j-1)*(key/2)+k ) )
                net.addLink( switch_ad, host )
    
    info("***starting network***\n")
    net.start()
    CLI(net)
    net.stop()
    
    
if __name__ == "__main__":
    setLogLevel("info")
    OVSKernelSwitch.setup()
    myTopo(4)