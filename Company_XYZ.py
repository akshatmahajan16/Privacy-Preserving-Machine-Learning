from Linear_Regression_model import Regression_Model
import phe as ph
import json
import os.path

""" Customer will keep his file data.json and upload here
this will check if file is present if not generate error"""


def getData():
    with open('customer_data.json', 'r') as file:
        d = json.load(file)
    data = json.loads(d)
    return data


def computeData():
    data = getData()
    mycoef = Regression_Model().getCoef()
    pk = data['public_key']
    pubkey = ph.PaillierPublicKey(n=int(pk['n']))
    enc_nums_rec = [ph.EncryptedNumber(pubkey, int(x[0], int(x[1]))) for x in data['values']]
    results = sum([mycoef[i] * enc_nums_rec[i] for i in range(len(mycoef))])
    return results, pubkey


""" This is the result generated by regression model and returned to customer """
# print(computeData()[0].ciphertext())

""" Now serilaize data ie encrypt data with public key and send back to customer"""


def serializeData():
    results, pubkey = computeData()
    encrypted_data = {}
    encrypted_data['pubkey'] = {'n': pubkey.n}
    encrypted_data['values'] = (str(results.ciphertext()), results.exponent)
    serialized = json.dumps(encrypted_data)
    return serialized


# print(serializeData())

""" Here if we verify the data that customer got so we can see that it is the same value."""
# data = age, hei, al, gen = [24, 4, 6, 1]
# mycoef = Regression_Model().getCoef()
# print(sum([data[i]*mycoef[i] for i in range(len(data))]))

def main():
    if os.path.exists('customer_data.json'):
        if not os.path.exists('result.json'):
            datafile = serializeData()
            with open('result.json', 'w') as file:
                json.dump(datafile, file)
    else:
        print("No Customer Data Available")


if __name__ == '__main__':
    main()
