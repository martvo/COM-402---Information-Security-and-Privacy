from flask import Flask, make_response, request
import hashlib, hmac
import base64

# Secret key of the HMAC is my password for hw1/ex1 encoded in utf8

key = "IwQEERtOXRMBCEQhRRgTAU8NSA==".encode("utf-8")

app = Flask(__name__)

@app.route('/ex3/login', methods=['POST'])
def login():
	if request.method == 'POST':
		if (request.is_json):
			content = request.get_json()
			username = content["user"]
			password = content["pass"]

			if username == "administrator" and password == "42":
				resp = make_response()
				returnString = username + ",1489662453,com402,hw2,ex3,administrator"
				h = hmac.new(key, returnString.encode("utf-8"), hashlib.sha256)
				returnString += "," + h.hexdigest()
				resp.set_cookie("LoginCookie", base64.b64encode(returnString.encode("utf-8")))
				return resp
			else:
				resp = make_response()
				returnString = username + ",1489662453,com402,hw2,ex3,user"
				h = hmac.new(key, returnString.encode("utf-8"), hashlib.sha256)
				returnString += "," + h.hexdigest()
				resp.set_cookie("LoginCookie", base64.b64encode(returnString.encode("utf-8")))
				return resp


@app.route("/ex3/list", methods=["POST"])
def list():
	if request.method == 'POST':
		cookie = request.cookies.get("LoginCookie")
		parts = base64.b64decode(cookie).decode("utf-8").rsplit(",", 1)

		h = hmac.new(key, parts[0].encode("utf-8"), hashlib.sha256)
		if h.hexdigest() != parts[1]:
			resp = make_response()
			resp.status_code = 403
			return resp

		status = parts[0].rsplit(",", 1)
		if status[1] == "administrator":
			resp = make_response()
			resp.status_code = 200
			return resp

		if status[1] == "user":
			resp = make_response()
			resp.status_code = 201
			return resp

		resp = make_response()
		resp.status_code = 400
		return resp


"""
curl -d '{"user": "martin.vold@epfl.ch", "pass": "IwQEERtOXRMBCEQhRRgTAU8NSA=="}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/ex3/login

"""

"""
curl -v --cookie "LoginCookie=
bWFydGluLnZvbGRAZXBmbC5jaCwxNDg5NjYyNDUzLGNvbTQwMixodzIsZXgzLHVzZXIsNDBmNTkwNDMyZmR
ZjM2Nzk2OTkxYzlhMTdkMmZjMDg2ZDU4ZDU5ZDUyYjUzZTczNDQwOGE5YjhjYWU0Y2IzNA==" 
http://127.0.0.1:5000/ex3/list

"""



"""
curl -d '{"user": "martin.vold@epfl.ch", "pass": "IwQEERtOXRMBCEQhRRgTAU8NSA=="}' 
-H "Content-Type: application/json" 
-X POST http://127.0.0.1:5000/ex3/login
"""


# (;_;)
'''
def HMAC(message):
	blockSize = 256

	if len(key) > hashlib.SHA256().block_size:
		key = hashlib.SHA256(key)

	oBlocK = ["0x5c" for i in range(hashlib.SHA256().block_size)]
	iBlock = ["0x35" for i in range(hashlib.SHA256().block_size)]

	oKeyPad = [a ^ b for a,b in zip(key, oBlocK)]
	iKeyPad = [a ^ b for a,b in zip(key, iBlock)]

	return hashlib.SHA256(joinString(oKeyPad, hashlib.SHA256(joinString(iKeyPad, message))));

def joinString(*args):
	return "".join(str(a) for a in args)
'''


if __name__ == "__main__":
	app.run()