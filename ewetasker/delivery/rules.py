import json
from data.sparql.rules import create_new_rule, get_all_user_rules, get_rule_by_uri, delete_rule
from delivery.channels import get_channel_with_action_uri, get_channel_with_event_uri
import logging
from rdflib import URIRef
log = logging.getLogger('tester.sub')
#log.warning('warning test')

# create rule
def create_rule(rule_json):
    rule_label = rule_json["rdfs:label"]
    rule_comment = rule_json["rdfs:comment"]
    rule_events = rule_json["events"]
    rule_actions = rule_json["actions"]
    rule_user_uri = rule_json["ewe:hasCreator"]
    return create_new_rule(rule_label, rule_comment, rule_events, rule_actions, rule_user_uri)

def get_user_rules(user_uri):

    rules = {"@context": { "@vocab" : "http://www.gsi.dit.upm.es/ontologies/ewe#"}, "rules" : []}
    user_rules_query = get_all_user_rules(user_uri)
    rules_uris = []
    for uri in user_rules_query:
        if uri[0] not in rules_uris:
            rules_uris.append(uri[0])
            actions=[]
            events=[]
            actionsChannels=[]
            eventsChannels=[]
            rule_query = get_rule_by_uri(uri[0])
            for label, comment, event, action, rule in rule_query:
                if event not in events:
                    events.append(event)
                    eventsChannels.append(get_channel_with_event_uri(event))
                if action not in actions:
                    actions.append(action)
                    actionsChannels.append(get_channel_with_action_uri(action))
            for label, comment, event, action, rule in rule_query:
                rules["rules"].append({"@id" : uri, "rdfs:label" : label.n3(), "rdfs:comment" : comment.n3(), "events" : events, "actions": actions, "rule" : rule.n3(), "actions channels": actionsChannels, "events channels": eventsChannels,  "user" : user_uri})
                break
    return json.dumps(rules).replace('\\"', "")

def delete_rule_with_uri(uri):
    return delete_rule(uri)