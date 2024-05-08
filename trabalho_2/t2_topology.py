#!/usr/bin/python

from __future__ import print_function

import os
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import dumpNodeConnections

class NetworkTopo(Topo):
    # Builds network topology
    def build(self, **_opts):

        s1 = self.addSwitch('s1', failMode='standalone')
        s2 = self.addSwitch('s2', failMode='standalone')
        s3 = self.addSwitch('s3', failMode='standalone')
        s4 = self.addSwitch('s4', failMode='standalone')
        s5 = self.addSwitch('s5', failMode='standalone')
        

        # Adding hosts
        h1 = self.addHost('h1',ip='192.168.0.1/28',mac='00:00:00:00:00:01')
        h2 = self.addHost('h2',ip='192.168.0.2/28',mac='00:00:00:00:00:02')
        h3 = self.addHost('h3',ip='192.168.0.3/28',mac='00:00:00:00:00:03')
        h4 = self.addHost('h4',ip='192.168.0.4/28',mac='00:00:00:00:00:04')
        h5 = self.addHost('h5',ip='192.168.0.5/28',mac='00:00:00:00:00:05')
        h6 = self.addHost('h6',ip='192.168.0.6/28',mac='00:00:00:00:00:06')


        # Connecting hosts to switches
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)
        self.addLink(s3, s5)
        self.addLink(s1, h1)
        self.addLink(s2, h2)
        self.addLink(s4, h3)
        self.addLink(s4, h4)
        self.addLink(s5, h5)
        self.addLink(s5, h6)

        #for d, s in [(d1, s1), (d2, s1)]:
        #    self.addLink(d, s)
topos = { 'mytopo': ( lambda: NetworkTopo() ) }

def inspect():
    net = Mininet(topo=NetworkTopo())
    net.start()
    CLI(net, script="sudo sh ./mininet/inspections.sh")
    net.stop()

def run():
   topo = NetworkTopo()
   print('aqui2')	
   net = Mininet(topo=topo, controller=None)
   
   net.start()
   h1 = net.get('h1')
   h2 = net.get('h2')
   h3 = net.get('h3')
   h4 = net.get('h4')
   h5 = net.get('h5')
   h6 = net.get('h6')
   s2 = net.get('s2')
   s3 = net.get('s3')
   s4 = net.get('s4')
   s5 = net.get('s5')
   
   # print("Letra b: inspecionando informações dos dispositivos e switchs conectados")
   
   '''print(h1.cmd('h1 ifconfig'))
   print(h2.cmd('h2 ifconfig'))
   print(h3.cmd('h3 ifconfig'))
   print(h4.cmd('h4 ifconfig'))
   print(h5.cmd('h5 ifconfig'))
   print(h6.cmd('h6 ifconfig'))
   print(s1.cmd('s1 ifconfig'))
   print(s2.cmd('s2 ifconfig'))
   print(s3.cmd('s3 ifconfig'))
   print(s4.cmd('s4 ifconfig'))
   print(s5.cmd('s5 ifconfig'))'''
   
   h1.cmd('sudo ovs-ofctl del-flows s1')
   h2.cmd('sudo ovs-ofctl del-flows s2')
   h3.cmd('sudo ovs-ofctl del-flows s4')
   h4.cmd('sudo ovs-ofctl del-flows s4')
   h5.cmd('sudo ovs-ofctl del-flows s5')
   h6.cmd('sudo ovs-ofctl del-flows s5')
   s2.cmd('sudo ovs-ofctl del-flows s1')
   s3.cmd('sudo ovs-ofctl del-flows s2')
   s4.cmd('sudo ovs-ofctl del-flows s3')
   s5.cmd('sudo ovs-ofctl del-flows s3')
   
   
   print('conexão de h1 com h2')
   
   net['s1'].cmd('sudo ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02,actions=output:1')
   net['s2'].cmd('sudo ovs-ofctl add-flow s2 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02,actions=output:3')
   
   net['s1'].cmd('sudo ovs-ofctl add-flow s1 dl_type=0x806,nw_proto=1,action=flood')
   net['s2'].cmd('sudo ovs-ofctl add-flow s2 dl_type=0x806,nw_proto=1,action=flood')
   
   net['s1'].cmd('sudo ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:01,actions=output:2')
   net['s2'].cmd('sudo ovs-ofctl add-flow s2 dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:01,actions=output:1')
   
   print(h1.cmd('sudo ovs-ofctl dump-flows s1'))
   print(h1.cmd('sudo ovs-ofctl dump-flows s2'))
   
   print('conexão de h3 com h4')
   
   net['s4'].cmd('sudo ovs-ofctl add-flow s4 dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:04,actions=output:3')
   net['s4'].cmd('sudo ovs-ofctl add-flow s4 dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:03,actions=output:2')
   
   print(h1.cmd('sudo ovs-ofctl dump-flows s4'))
   
   print('conexão de h3 para h5')
   
   net['s4'].cmd('sudo ovs-ofctl add-flow s4 dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:05,actions=output:1')
   net['s3'].cmd('sudo ovs-ofctl add-flow s3 dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:05,actions=output:3')
   net['s5'].cmd('sudo ovs-ofctl add-flow s5 dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:05,actions=output:2')
   
   net['s4'].cmd('sudo ovs-ofctl add-flow s4 dl_src=00:00:00:00:00:05,dl_dst=00:00:00:00:00:03,actions=output:2')
   net['s3'].cmd('sudo ovs-ofctl add-flow s3 dl_src=00:00:00:00:00:05,dl_dst=00:00:00:00:00:03,actions=output:2')
   net['s5'].cmd('sudo ovs-ofctl add-flow s5 dl_src=00:00:00:00:00:05,dl_dst=00:00:00:00:00:03,actions=output:1')
   
   print(h1.cmd('sudo ovs-ofctl dump-flows s3'))
   print(h1.cmd('sudo ovs-ofctl dump-flows s4'))
   print(h1.cmd('sudo ovs-ofctl dump-flows s5'))
   
   net['s1'].cmd('sudo ovs-ofctl add-flow s1 dl_type=0x806,nw_proto=1,action=flood')
   net['s2'].cmd('sudo ovs-ofctl add-flow s2 dl_type=0x806,nw_proto=1,action=flood')
   net['s3'].cmd('sudo ovs-ofctl add-flow s3 dl_type=0x806,nw_proto=1,action=flood')
   net['s4'].cmd('sudo ovs-ofctl add-flow s4 dl_type=0x806,nw_proto=1,action=flood')
   net['s5'].cmd('sudo ovs-ofctl add-flow s5 dl_type=0x806,nw_proto=1,action=flood')
   
   
   print(h1.cmd('sudo ovs-ofctl dump-flows s1'))
   print(h1.cmd('sudo ovs-ofctl dump-flows s2'))
   print(h1.cmd('sudo ovs-ofctl dump-flows s3'))
   print(h1.cmd('sudo ovs-ofctl dump-flows s4'))
   print(h1.cmd('sudo ovs-ofctl dump-flows s5'))
   
   CLI(net)
   net.stop()
   
if __name__ == '__main__':
    setLogLevel('info')
    #inspect()
    run()
