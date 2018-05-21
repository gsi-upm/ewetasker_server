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
    endpoint = 'http://localhost:3030/ewetaskerdataset/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Get channels
    rq = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>


        SELECT ?subject ?label ?comment ?logo
        WHERE {
        ?subject rdfs:subClassOf ewe:Channel ;
                rdfs:label ?label ;
                rdfs:comment ?comment .
        
        OPTIONAL {?subject foaf:logo ?logo }
        }
    """

    channels = { "channels" : []}
    channels_result = store.query(rq)
    for s, l, c, lo in channels_result:
        # TODO: get channel logo
        channels["channels"].append({"@id" : s.n3(), "rdfs:label" : l.n3(), "rdfs:comment" : c.n3()})
        # TODO: get events and actions

    #print(channels)
    #print(store.query(rq).serialize(format='json-ld', indent=4))
    return json.dumps(channels)