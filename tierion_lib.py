import requests
import json
# import TierionCaller
import hashlib
from time import sleep
from merkletools import MerkleTools

class TierionHash:

    def __init__(self, name ,password):
        self.hashAuthEndpoint='https://hashapi.tierion.com/v1/auth/token'
        self.HashAuth=requests.post(self.hashAuthEndpoint,data = {'username':name,'password':password})

    def refresh(self):
        data=self.HashAuth.json()
        token=data['refresh_token']
        self.HashAuth=requests.post('https://hashapi.tierion.com/v1/auth/refresh', data={'refreshToken':token})

    def submitHashItem(self, item):
        try:
            hashedItem= hashlib.sha256(item.encode('utf-8')).hexdigest()
            data=self.HashAuth.json()
            token=data['access_token']
            payload={'hash':hashedItem}
            headers = {'Authorization':"Bearer "+token}
            receipt=requests.post('https://hashapi.tierion.com/v1/hashitems', headers=headers, data=payload)
            return receipt.json()['receiptId']
        except Exception as e:
            print('No connection. Error code: '+repr(e))
            raise e


    def getReceipt(self, id_receipt):
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
    def getAllBlockSubscriptions(self):
        try:
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            allBlockSubscription=requests.get('https://hashapi.tierion.com/v1/blocksubscriptions',headers=headers)
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e

    def getBlockSubscription(self, id):
        try:
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            response=requests.get('https://hashapi.tierion.com/v1/receipts/'+id,headers=headers)
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e

    def createBlockSubscription(self,callback,newLabel):
        try:
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            response=requests.post('https://hashapi.tierion.com/v1/blocksubscriptions',headers=headers,data = {'callbackUrl':callback,'label':newLabel})
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e

    def updateBlockSubscription(self,id,callback,newLabel):
        try:
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            response=requests.get('https://hashapi.tierion.com/v1/blocksubscriptions/'+id,headers=headers,data = {'callbackUrl':callback,'label':newLabel})
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e

    def deleteBlockSubscription(self,id,callback,newLabel):
        try:
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            response=requests.delete('https://hashapi.tierion.com/v1/blocksubscriptions/'+id,headers=headers)
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e
