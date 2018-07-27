from pymongo import *
import configparser
from jwt import (
    JWT,
    jwk_from_dict,
    jwk_from_pem,
)
import json

config = configparser.ConfigParser()
config.read('config/config.ini')
users = MongoClient('mongodb://'+ config['MONGODB']['BASE_URL'] +':27017/').ewetaskerdb.users

with open('certs/lab.cluster.gsi.dit.upm.es.pem', 'rb') as fh:
    signing_key = jwk_from_pem(fh.read())
jwt = JWT()

def create_user(username, password):
    if users.find({'user':username}).count()==0:
        new_user={
            'user': username,
            'password': password,
            'rules':[],
            'channels':[]
        }
        users.insert_one(new_user)
        return jwt.encode({'username':username, 'rules':[],'channels':[]}, signing_key, 'RS256')
    return '0'

def login_user(username, password):
    user = users.find_one({'user':username, 'password':password})
    if(user!=None):
        return jwt.encode({'username':username, 'rules':user['rules'],'channels':user['channels']}, signing_key, 'RS256')
    return '0'

def remove_user(username, password):
    if users.find({'user':username, 'password':password}).count():
        users.delete_one({"user":username, "password":password})
        return '1'
    return '0'
