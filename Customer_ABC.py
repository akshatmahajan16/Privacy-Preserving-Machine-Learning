import phe as ph
import json
import easygui
import os.path

def Generate_keys():
    public_key, private_key = ph.generate_paillier_keypair()
    keys={}
    keys['public_key'] = {'n': public_key.n}
    keys['private_key'] = {'p': private_key.p,'q':private_key.q}
    with open('custkeys.json', 'w') as file:
        json.dump(keys, file)

# Generate_keys()
def Fetch_keys():
    with open('custkeys.json', 'r') as file:
        keys=json.load(file)
        pub_key=ph.PaillierPublicKey(n=int(keys['public_key']['n']))
        priv_key=ph.PaillierPrivateKey(pub_key,keys['private_key']['p'],keys['private_key']['q'])
        return pub_key, priv_key

""" Encrypting customer data with public key and dumping as json"""
def Data_serialization(public_key, data):
    encrypted_data_list = [public_key.encrypt(x) for x in data]
    encrypted_data={}
    encrypted_data['public_key'] = {'n': public_key.n}
    encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in         encrypted_data_list]
    serialized = json.dumps(encrypted_data)
    return serialized

def load_Result():
    with open('result.json', 'r') as file:
        ans=json.load(file)
        answer=json.loads(ans)
        return answer


if not os.path.exists('custkeys.json'):
    Generate_keys()

if not os.path.exists('customer_data.json'):
    pub_key, priv_key = Fetch_keys()
    data = age, hei, al, gen = [24, 4, 6, 1]
    Data_serialization(pub_key, data)
    datafile = Data_serialization(pub_key, data)
    with open('customer_data.json', 'w') as file:
        json.dump(datafile, file)

if os.path.exists('result.json'):
    pub_key, priv_key = Fetch_keys()
    answer_file = load_Result()
    answer_key = ph.PaillierPublicKey(n=int(answer_file['pubkey']['n']))
    answer = ph.EncryptedNumber(answer_key, int(answer_file['values'][0]), int(answer_file['values'][1]))
    if (answer_key == pub_key):
        print(priv_key.decrypt(answer))
        easygui.msgbox(f"{priv_key.decrypt(answer)}", title="Predicted Value")
else:
    print("Waiting for Result")