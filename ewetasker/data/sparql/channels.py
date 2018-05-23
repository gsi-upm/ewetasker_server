from rdflib import Graph, Literal, URIRef, plugin
from rdflib.namespace import RDF, SKOS
from rdflib.plugins.stores import sparqlstore
from rdflib.plugins.parsers.notation3 import N3Parser
from SPARQLWrapper import SPARQLWrapper, JSON, JSONLD
from rdflib.serializer import Serializer
from rdflib.plugins.serializers.n3 import N3Serializer
import json

def get_all_channels():

    #Define the SparQL store
    endpoint = 'http://localhost:3030/ewetasker/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Get channels
    get_channels_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>


        SELECT ?channel ?label ?comment ?logo
        WHERE {
        ?channel rdfs:subClassOf ewe:Channel ;
                rdfs:label ?label ;
                rdfs:comment ?comment .
        
        OPTIONAL {?channel foaf:logo ?logo }
        }
    """

    
    channels = { "channels" : []}
    channels_result = store.query(get_channels_query)
    index = 0
    for uri, label, comment, logo in channels_result:
        # TODO: get channel logo
        channels["channels"].append({"@id" : uri, "rdfs:label" : label.n3(), "rdfs:comment" : comment.n3(), "events" : [], "actions" : []})
        
        # TODO: get actions and channels parameters
        
        # get actions
        get_actions_query = """
            PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?action ?label ?comment
            WHERE {
            ?action rdfs:subclassOf ewe:Action ;
                    rdfs:domain %s;
                    rdfs:label ?label ;
                    rdfs:comment ?comment .
            }
        """ % (uri.n3())
        actions_result = store.query(get_actions_query)
        for action_uri, action_label, action_comment in actions_result:
            channels["channels"][index]["actions"].append({"@id" : action_uri, "rdfs:label" : action_label.n3(), "rdfs:comment" : action_comment.n3()})

        # get events
        get_events_query = """
            PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?action ?label ?comment
            WHERE {
            ?action rdfs:subclassOf ewe:Event ;
                    rdfs:domain %s;
                    rdfs:label ?label ;
                    rdfs:comment ?comment .
            }
        """ % (uri.n3())
        events_result = store.query(get_events_query)
        for event_uri, event_label, event_comment in events_result:
            channels["channels"][index]["events"].append({"@id" : event_uri, "rdfs:label" : event_label.n3(), "rdfs:comment" : event_comment.n3()})

        index+=1
    #print(channels)
    #print(store.query(rq).serialize(format='json-ld', indent=4))
    return json.dumps(channels)