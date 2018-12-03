from data.sparql.users import *
from rdflib import Graph
import json

def add_user(username):
    return create_new_user(username)


def get_user(username):
    user_result=query_user(username)
    user=[]

    for uri in user_result:
        user.append({"@id" : uri})

    return json.dumps(user).replace('\\"', "")

def remove_user(username):
    return delete_user(username)