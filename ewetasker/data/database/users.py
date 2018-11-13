from pymongo import *
from jwt import (
    JWT,
    jwk_from_dict,
    jwk_from_pem,
)
import json
from delivery.users import *
import os

users = MongoClient('mongodb://'+ os.environ['MONGODB_URL'] +'/').ewetaskerdb.users

if os.environ.get('EWE_PEM') is not None:
    signing_key=os.environ.get('EWE_PEM')
else:
    with open(os.environ['CERTS_PATH'], 'rb') as fh:
        signing_key = jwk_from_pem(fh.read())
jwt = JWT()

def create_user(username, password):
    if users.find({'user':username}).count()==0:
        new_user={
            'user': username,
            'password': password
        }
        users.insert_one(new_user)
        add_user(username)
        data=get_user(username)
        return jwt.encode({'username':username, 'data':data}, signing_key, 'RS256')
    return '0'

def login_user(username, password):
    try:
        user = users.find_one({'user':username, 'password':password})
    except Exception:
        user=None
        return '2'
    if(user!=None):
        data=get_user(username)
        return jwt.encode({'username':username, 'data':data}, signing_key, 'RS256')
    return '0'

def drop_user(username, password):
    if users.find({'user':username, 'password':password}).count():
        users.delete_one({"user":username, "password":password})
        remove_user(username)
        return '1'
    return '0'

