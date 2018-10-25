from elasticsearch import Elasticsearch
from twisted.logger import Logger
import time
import pprint
import os
import json
import datetime
import rdflib
from rdflib import Graph
import logging
log = logging.getLogger('tester.sub')
ID_events=0
ID_actions=0
try:
    time.sleep(30)
    es = Elasticsearch(hosts=[{'host': os.environ['ES_ENDPOINT'], 'port': os.environ['ES_ENDPOINT_PORT']}])
    connected = es.ping()
    log.warning("Correctly connected to elasticsearch:"+ str(connected)+"")
    count = es.count("ewetasker", doc_type="events")
    ID_events = count["count"]
    log.warning("Number of events already registered:"+ str(ID_events)+"")
    count = es.count("ewetasker", doc_type="actions")
    ID_actions = count["count"]
    log.warning("Number of events already registered:"+ str(ID_actions)+"")
except Exception as e:
    log.warning("Error connecting to elasticsearch")
    log.warning(e)

def upload_event_to_es(username, event):
    log.warning('Uploading events to ES')
    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX math: <http://www.w3.org/2000/10/swap/math#>
        PREFIX string: <http://www.w3.org/2000/10/swap/string#>
        
        SELECT ?uri ?param ?value ?eventType ?paramType ?channel
        WHERE {
            ?uri rdf:type ewe:Event ;
                 rdf:type ?eventType ;
                 ewe:hasParameter ?param ;
                 rdfs:domain ?channel .
            ?param rdf:type ?paramType .
            ?param rdf:value ?value .
        }
    """
    g = Graph()
    kwargs={}
    events = []
    parameters = {}
    lastEvent = ""
    lastChannel = ""
    try:
        g.parse(format="n3", data=event)
        event_query = g.query(query)
        for uri, param, value, eventType, paramType, channel in event_query:
            if(eventType.n3()!="<http://gsi.dit.upm.es/ontologies/ewe/ns/Event>"):
                if(lastEvent!=eventType)&(lastEvent!=""):
                    events.append({"param": parameters, "event": lastEvent.split("/")[-1], "channel": lastChannel.split("/")[-1]})
                    parameters = {}
                parameters[paramType.split("/")[-1]] = value
                lastEvent = eventType
                lastChannel = channel
        events.append({"param": parameters, "event": lastEvent.split("/")[-1], "channel": lastChannel.split("/")[-1]})
    except Exception as e:
        log.warning(e)
        return ""
    events_json = json.dumps(events).replace('\\"', "")
    events_json=json.loads(events_json)
    try:
        count = es.count("ewetasker")
        ID_events = count["count"]
    except Exception as e:
        ID_events=0
        
    for event in events_json:
        ID_events += 1
        kwargs={}
        kwargs["param"] = event["param"]
        kwargs["channel"] = event["channel"]
        kwargs["event"] = event["event"]
        kwargs['eventId'] = ID_events
        kwargs['time'] = datetime.datetime.now().hour
        kwargs["user"] = username
        kwargsJson = json.dumps(kwargs)
        res = es.index(index='ewetasker', doc_type='events', id=ID_events, body=kwargsJson)
        log.warning("  ")
        log.warning("Event Loaded to ElasticSearch:")
        pprint.PrettyPrinter(indent=2).pprint(kwargs)
    return ""

def upload_action_to_es(username, actions_json):
    log.warning('Uploading actions to ES')
    actions_json = json.loads(actions_json)
    try:
        count = es.count("ewetasker")
        ID_actions = count["count"]
    except Exception as e:
        ID_actions=0
    if (actions_json["success"]==0):
        log.warning("no hay acciones")
        return ''
    for action in actions_json["actions"]:
        ID_actions += 1
        kwargs={}
        kwargs["param"] = action["parameters"]
        kwargs["channel"] = action["channel"]
        kwargs["action"] = action["action"]
        kwargs['actionId'] = ID_actions
        kwargs['time'] = datetime.datetime.now().hour
        kwargs["user"] = username
        kwargsJson = json.dumps(kwargs)
        res = es.index(index='ewetasker', doc_type='actions', id=ID_actions, body=kwargsJson)
        log.warning("  ")
        log.warning("Action Loaded to ElasticSearch:")
        pprint.PrettyPrinter(indent=2).pprint(kwargs)
    return ""