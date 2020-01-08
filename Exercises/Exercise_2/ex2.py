import asyncio
import websockets
import binascii
import random
import hashlib
import uuid


import asyncio
import websockets

async def ex2():
    async with websockets.connect('ws://com402.epfl.ch/hw2/ws') as websocket:

    	password = "IwQEERtOXRMBCEQhRRgTAU8NSA==".encode()
    	U = "martin.vold@epfl.ch".encode()
    	H = "sha256"
    	N = int("EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3", 16)
    	g = 2
    	
    	#First send
    	await websocket.send(U)
    	print(f"> Sendt email as encoded: {U}")


    	#First receive
    	ecoded_salt = await websocket.recv()
    	print(f"> Received salt (decoded): {ecoded_salt}")
    	salt, s_buff = decode_number(ecoded_salt)
    	print(f"> Received salt (decoded): {salt}")


    	#Second send
    	a = cryptrand()
    	A = pow(g, a, N)
    	encoded_A, a2 = encode_number(A)
    	await websocket.send(encoded_A)
    	print(f"> Sendt A as encoded: {A}")


    	#Second receive
    	encoded_B = await websocket.recv()
    	B, b = decode_number(encoded_B)
    	print(f"> Received B (decoded): {B}")


    	#Create session key
    	u = hashlib.sha256(a2 + b).hexdigest()
    	tmp = hashlib.sha256(U + b':' + password).hexdigest()
    	x = hashlib.sha256(s_buff + binascii.unhexlify(tmp)).hexdigest()
    	S = pow(B - pow(g, int(x, 16), N), a + int(u, 16)*int(x, 16), N)
    	print(f"> Session Key: {S}")
    	S_encoded, sec = encode_number(S)


    	#Last send, full send
    	to_send = hashlib.sha256(a2 + b + sec)
    	await websocket.send(to_send.hexdigest())  # May need to encode
    	token = await websocket.recv()
    	print(f"> Token: {token}")




def cryptrand(n=256):
	return random.SystemRandom().getrandbits(n)

def encode_number(to_send):
	buff = to_send.to_bytes((to_send.bit_length() + 7) // 8, 'big')
	return binascii.hexlify(buff).decode(), buff

def decode_number(encoded_number):
	buff = binascii.unhexlify(encoded_number)
	return int.from_bytes(buff, 'big'), buff


asyncio.get_event_loop().run_until_complete(ex2())
