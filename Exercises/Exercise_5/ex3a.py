import requests
import json
from phe import paillier


get_input_addr = "http://com402.epfl.ch/hw5/ex3/get_input"
prediction_service_addr = "http://com402.epfl.ch/hw5/ex3/securehealth/prediction_service"
get_token_addr = "http://com402.epfl.ch/hw5/ex3/get_token_1"
data = { "email": "martin.vold@epfl.ch" }

post = requests.post(get_input_addr, json=data)

# Get the vector from the response
vector = json.loads(post.text)["x"]
print("Vector: {}".format(vector))

# Get keys for the encryption
public_key, private_key = paillier.generate_paillier_keypair()

# Encrypt the numbers in the list
encrypted_number_list = [public_key.encrypt(x).ciphertext() for x in vector]

prediction_data = { "email": "martin.vold@epfl.ch", "pk": public_key.n, "encrypted_input": encrypted_number_list, "model": 1 }
post2 = requests.post(prediction_service_addr, json=prediction_data)

# Get the encrypted prediction
encrypted_prediction = json.loads(post2.text)["encrypted_prediction"]
# print("Encrypted predicion: {}".format(encrypted_prediction))

# Decrypt the prediction and deliver it for the token
pred = paillier.EncryptedNumber(public_key, encrypted_prediction)
decrypted_prediction = private_key.decrypt(pred)
# print("Decrypted prediction: {}".format(decrypted_prediction))

token_data = {"email": "martin.vold@epfl.ch", "prediction": decrypted_prediction }
post3 = requests.post(get_token_addr, json=token_data)
token = json.loads(post3.text)["token"]
print(token)