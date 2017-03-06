import requests
import json
# import TierionCaller
import hashlib
from time import sleep
from merkletools import MerkleTools

class TierionHash:

    def __init__(self, name ,password):
        self.hashAuthEndpoint='https://hashapi.tierion.com/v1/auth/token'
        self.password=password
        self.nameUser=name
        self.HashAuth=requests.post(self.hashAuthEndpoint,data = {'username':self.nameUser,'password':self.password})

    def refresh(self):
        data=self.HashAuth.json()
        token=data['refresh_token']
        self.HashAuth=requests.post('https://hashapi.tierion.com/v1/auth/refresh', data={'refreshToken':token})

    def submit_hash_item(self, item):
        try:
            hashedItem= hashlib.sha256(item.encode('utf-8')).hexdigest()
            data=self.HashAuth.json()
            token=data['access_token']
            payload={'hash':hashedItem}
            headers = {'Authorization':"Bearer "+token}
            receipt=requests.post('https://hashapi.tierion.com/v1/hashitems', headers=headers, data=payload)
            return receipt.json()['receiptId']
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e


    def get_receipt(self, id_receipt):
        try:
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            print(id_receipt)
            receipt=requests.get('https://hashapi.tierion.com/v1/receipts/'+id_receipt,headers=headers)
            return receipt.json()['receipt']
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e
    def get_all_blocksubscritption(self):
        try:
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            allBlockSubscription=requests.get('https://hashapi.tierion.com/v1/blocksubscriptions',headers=headers)
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e

    def get_block_subscription(self, id):
        try:
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            response=requests.get('https://hashapi.tierion.com/v1/receipts/'+id,headers=headers)
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e

    def create_callBack_subscriptioin(self,callback,newLabel):
        try:
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            response=requests.post('https://hashapi.tierion.com/v1/blocksubscriptions',headers=headers,data = {'callbackUrl':callback,'label':newLabel})
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e

    def update_block_subscription(self,id,callback,newLabel):
        try:
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            response=requests.get('https://hashapi.tierion.com/v1/blocksubscriptions/'+id,headers=headers,data = {'callbackUrl':callback,'label':newLabel})
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e

    def delete_block_subscription(self,id,callback,newLabel):
        try:
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            response=requests.delete('https://hashapi.tierion.com/v1/blocksubscriptions/'+id,headers=headers)
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e

def validate_tierion_receipt(us_original_file, receipt_dict):
    url = 'https://blockchain.info/rawtx/{}'.format(receipt_dict['anchors'][0]['sourceId'])
    try:
        trx_dict = requests.get(url, headers={'content-type': 'application/json'}).json()
    except:
        return (False, False, False)
    # 1: check that the merkle root exists as the OP_RETURN value of the ouput[0] script
    b_in_blockchain = '6a20'+receipt_dict['merkleRoot'] == trx_dict['out'][0]['script']
    mt = MerkleTools()
    b_proof_valid = mt.validate_proof(receipt_dict['proof'], receipt_dict['targetHash'], receipt_dict['merkleRoot'])
    b_hashes_match = hashlib.sha256(us_original_file.encode('utf-8')).hexdigest() == receipt_dict['targetHash']
    return b_in_blockchain, b_proof_valid, b_hashes_match
