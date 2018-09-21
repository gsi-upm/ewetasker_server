from data.sparql.rules import get_all_user_rules, get_rule_by_uri
from rdflib import Graph
import configparser
import logging
import json
import requests
config = configparser.ConfigParser()
config.read('config/config.ini')
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
    return post_to_eye_server(event_evaluated, rules)
    


def post_to_eye_server(event, rules):
    payload = {'data': event, 'query':rules}
    url = 'http://' + config['EYE']['BASE_URL']
    response = requests.post(url, data=payload)
    return (response.text, response.status_code, response.headers.items())