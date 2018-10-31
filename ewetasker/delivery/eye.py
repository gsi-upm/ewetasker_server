from data.sparql.rules import get_all_user_rules, get_rule_by_uri
from actuator.performer_manager import select_performer
from rdflib import Graph
import configparser
import logging
import json
import requests
from data.elasticsearch.ewe_es import upload_action_to_es 
import os
log = logging.getLogger('tester.sub')


def evaluate_event(username, event_evaluated):
    user_uri = "http://gsi.dit.upm.es/ontologies/ewe/ns/"+username
    user_rules_query = get_all_user_rules(user_uri)
    rules =""
    rules_uris = []
    for uri in user_rules_query:
        if uri[0] not in rules_uris:
            rules_uris.append(uri[0])
            rule_query = get_rule_by_uri(uri[0])
            for label, comment, event, action, rule in rule_query:
                rules += " " + rule
                break
    return parse_result(username,post_to_eye_server(event_evaluated, rules))
    


def post_to_eye_server(event, rules):
    payload = {'data': event, 'query':rules}
    url = 'http://' + os.environ['EYE_URL']+'/'
    response = requests.post(url, data=payload)
    return response.text
    #return response.text, response.status_code, response.headers.items())

def parse_result(username, result):
    result = result.replace("PREFIX", "@prefix", 3)
    result = result.replace(">", "> .", 3)
    query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT ?uri ?param ?value ?actionType ?paramType ?channel
            WHERE {
                ?uri rdf:type ewe:Action ;
                    rdf:type ?actionType ;
                    ewe:hasParameter ?param ;
                    rdfs:domain ?channel .
                ?param rdf:type ?paramType . 
                ?param rdf:value ?value .
            }
    """
    g = Graph()
    g.parse(format="n3", data=result)
    if (len(g)>0):
        success = 1
    else:
        success = 0
    rule_query = g.query(query)
    actions = {"success": success, "actions" : []}
    parameters = {}
    lastAction = ""
    lastUri = ""
    lastChannel = ""
    for uri, param, value, actionType, paramType, channel in rule_query:
        if(actionType.n3()!="<http://gsi.dit.upm.es/ontologies/ewe/ns/Action>"):
            if(lastAction!=actionType)&(lastAction!=""):
                actions["actions"].append({"@id" : lastUri, "parameters": parameters, "action": lastAction.split("/")[-1], "channel": lastChannel.split("/")[-1]})
                parameters = {}
            parameters[paramType.split("/")[-1]] = value
            lastAction = actionType
            lastUri = uri
            lastChannel = channel
    actions["actions"].append({"@id" : lastUri, "parameters": parameters, "action": lastAction.split("/")[-1], "channel": lastChannel.split("/")[-1]})
    actions_json = json.dumps(actions).replace('\\"', "")
    upload_action_to_es(username, actions_json)
    select_performer(actions_json)
    return actions_json