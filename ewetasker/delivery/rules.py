import json
from data.sparql.rules import create_new_rule

# create rule
def create_rule(rule_json):
    print(rule_json)
    rule_label = rule_json["rdfs:label"]
    rule_comment = rule_json["rdfs:comment"]
    rule_events = rule_json["events"]
    rule_actions = rule_json["actions"]

    return create_new_rule(rule_label, rule_comment, rule_events, rule_actions)