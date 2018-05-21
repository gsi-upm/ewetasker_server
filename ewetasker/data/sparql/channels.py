from rdflib import Graph, Literal, URIRef, plugin
from rdflib.namespace import RDF, SKOS
from rdflib.plugins.stores import sparqlstore
from rdflib.plugins.parsers.notation3 import N3Parser
from SPARQLWrapper import SPARQLWrapper, JSON, JSONLD
from rdflib.serializer import Serializer
from rdflib.plugins.serializers.n3 import N3Serializer
import json

def get_all_channels():
    #Define the Stardog store
    endpoint = 'http://localhost:3030/ewetaskerdataset/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))
    #Identify a named graph where we will be adding our instances.
    #default_graph = Graph()
    #ng = Graph(store, identifier='default')
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
        LIMIT 25
    """

    channels = { "channels" : []}
    for s, l, c, lo in store.query(rq):
        channels["channels"].append({"@id" : s.n3(), "rdf:label" : l.n3()})
        print(s)
        print(l)
        print(c)
        print(lo)


    print(channels)
    #print(store.query(rq).serialize(format='json-ld', indent=4))
    return ""