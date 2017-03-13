import requests
import json
# import TierionCaller
import sys, getopt
import datetime

import hashlib
from time import sleep

class TierionHash:

    def __init__(self, name ,password):
        self.hashAuthEndpoint='https://hashapi.tierion.com/v1/auth/token'
        self.HashAuth=requests.post(self.hashAuthEndpoint,data = {'username':name,'password':password})
        self.expires_at=datetime.datetime.now()+ datetime.timedelta(0,self.HashAuth.json()['expires_in'])

    def refresh(self):
        data=self.HashAuth.json()
        token=data['refresh_token']
        self.HashAuth=requests.post('https://hashapi.tierion.com/v1/auth/refresh', data={'refreshToken':token})
        self.expires_at=datetime.datetime.now()+ datetime.timedelta(0,self.HashAuth.json()['expires_in'])


    def submitHashItem(self, item):
        try:
            if(self.expired_auth()):
                self.refresh()
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
            if(self.expired_auth()):
                self.refresh()
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            url='https://hashapi.tierion.com/v1/receipts/'+id_receipt
            receipt=requests.get(url,headers=headers)
            return receipt.json()
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e


    def getAllBlockSubscriptions(self):
        try:
            if(self.expired_auth()):
                self.refresh()
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            allBlockSubscription=requests.get('https://hashapi.tierion.com/v1/blocksubscriptions',headers=headers)
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e

    def getBlockSubscription(self, id):
        try:
            if(self.expired_auth()):
                self.refresh()
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            response=requests.get('https://hashapi.tierion.com/v1/receipts/'+id,headers=headers)
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e

    def createBlockSubscription(self,callback,newLabel):
        try:
            if(self.expired_auth()):
                self.refresh()
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            response=requests.post('https://hashapi.tierion.com/v1/blocksubscriptions',headers=headers,data = {'callbackUrl':callback,'label':newLabel})
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e

    def updateBlockSubscription(self,id,callback,newLabel):
        try:
            if(self.expired_auth()):
                self.refresh()
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            response=requests.get('https://hashapi.tierion.com/v1/blocksubscriptions/'+id,headers=headers,data = {'callbackUrl':callback,'label':newLabel})
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e

    def deleteBlockSubscription(self,id,callback,newLabel):
        try:
            if(self.expired_auth()):
                self.refresh()
            data=self.HashAuth.json()
            token=data['access_token']
            headers = {'Authorization':"Bearer "+token}
            response=requests.delete('https://hashapi.tierion.com/v1/blocksubscriptions/'+id,headers=headers)
        except Exception as e:
            print('No connection. Got an error code: '+repr(e))
            raise e


    def expired_auth(self):
        if(self.HashAuth.json()['access_token'] and self.HashAuth.json()['refresh_token'] and self.expires_at < datetime.datetime.now()):
            return True
        else:
            return False

    def main(self):
        print(self.HashAuth.json())
        print(self.hashAuthEndpoint)
        self.refresh()
        print(self.expired_auth())
        print(self.HashAuth.json())
        reciept=self.submitHashItem('test')
        print(reciept)
        itemReciept=self.getReceipt(reciept)
        print(itemReciept)


if __name__ == "__main__":
    print(sys.argv[1])
    print(sys.argv[2])
    test = TierionHash(sys.argv[1],sys.argv[2])
    test.main()
