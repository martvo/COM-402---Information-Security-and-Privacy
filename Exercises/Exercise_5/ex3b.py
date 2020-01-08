import requests
import json
import sys
import random
from phe import paillier
from sklearn.linear_model import LinearRegression


addr = "http://com402.epfl.ch/hw5/ex3/securehealth/prediction_service"
get_token_addr = "http://com402.epfl.ch/hw5/ex3/get_token_2"

public_key, private_key = paillier.generate_paillier_keypair()
data = { "email": "martin.vold@epfl.ch", "pk": public_key.n, "encrypted_input": [], "model": 2 }

# Query the model for every possible input and calculate the parameters
# Number of possible queries is 2^12 = 4096 as the lenght of the input vector is 12
# Might only choose a subset with cardinality ~13 of the numbers between 0 and 4096
x_list = []
y_list = []
my_range = range(4096)

# Choose sample from all possible inputs, without replacement
# Use choises for sample with replacement
my_choices = random.sample(my_range, 14)

counter = 0
for i in my_choices:

	# Turn the int to a list of its bits
	vector = [1 if digit == "1" else 0 for digit in bin(i)[2:]]

	# If length of vector is less than 12, pad it with 0's at the start
	if len(vector) != 12:
		pad = 12 - len(vector)
		pad_list = [0 for x in range(pad)]
		vector = pad_list + vector

	# Fanzy write
	sys.stdout.write("\r{}, {}".format(vector, counter))
	sys.stdout.flush()

	# Encrypt the input vector, post and decrypt response
	encrypted_number_list = [public_key.encrypt(x).ciphertext() for x in vector]
	data["encrypted_input"] = encrypted_number_list
	post = requests.post(addr, json=data)
	encrypted_prediction = json.loads(post.text)["encrypted_prediction"]
	pred = paillier.EncryptedNumber(public_key, encrypted_prediction)
	decrypted_prediction = private_key.decrypt(pred)

	x_list.append(vector)
	y_list.append(decrypted_prediction)
	counter += 1

print()

# Fit the linear regressior to our acquired data
reg = LinearRegression().fit(x_list, y_list)

# Post and receive the token!
integer_weights = [round(x) for x in reg.coef_.tolist()]
integer_bias = round(reg.intercept_)
token_data = {"email": "martin.vold@epfl.ch", "weights": integer_weights, "bias": integer_bias }
post = requests.post(get_token_addr, json=token_data)
token = json.loads(post.text)["token"]
print(token)