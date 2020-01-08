
from flask import Flask, request, make_response
# from flask.ext.bcrypt import Bcrypt
import bcrypt
import sys


app = Flask(__name__)
# bcrypt = Bcrypt(app)

@app.route('/hw4/ex2', methods=['POST'])
def crypt():
	if (request.is_json):
		print("Request was JSON")
		content = request.get_json()
		username = content["user"]
		password = content["pass"]

		print("User name is: {}, password is: {}".format(username, password))

		password = password.encode("utf-8")
		print("Password after UTF-8 encoding: {}".format(password))

		crypted = bcrypt.hashpw(password, bcrypt.gensalt())
		print("Password after bcrypt: {}".format(crypted.decode()))
		respons = make_response()
		respons.status_code = 200
		respons.set_data = crypted.decode()
		return crypted, 200  # can return both the decoded and undecoded hashed password




if __name__ == "__main__":
	app.run()




"""
curl -d '{"user": "martin.vold@epfl.ch", "pass": "Hello World"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/hw4/ex2

"""