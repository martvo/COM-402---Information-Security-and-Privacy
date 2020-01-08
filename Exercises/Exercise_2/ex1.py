from flask import Flask
from flask import request
from flask import make_response
import base64
import sys

app = Flask(__name__)

@app.route('/hw2/ex1', methods=['POST'])
def login():
    if request.method == 'POST':
    	mySecureOneTimePad = "Never send a human to do a machine's job"
    	if (request.is_json):
    		content = request.get_json()
    		username = content["user"]
    		password = content["pass"]

    		if len(username) > 100 or len(password) > 100:
    			response = make_response()
    			response.status_code = 400
    			return response

    		if len(mySecureOneTimePad) < len(username):
    			diff = len(username) - len(mySecureOneTimePad)
    			mySecureOneTimePad += mySecureOneTimePad[:diff]

    		ascii_username = list(map(ord, username))
    		ascii_pad = list(map(ord, mySecureOneTimePad[:len(username)]))

    		xor_array = [a ^ b for a,b in zip(ascii_username, ascii_pad)]

    		new_string = "".join(map(chr, xor_array))

    		base64_encoded_string = base64.b64encode(new_string.encode("utf-8"))

    		if base64_encoded_string.decode() != password:
    			response = make_response()
    			response.status_code = 400
    			return response

    		response = make_response()
    		response.status_code = 200
    		return response



if __name__ == "__main__":
	app.run()