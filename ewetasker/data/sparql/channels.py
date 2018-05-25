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

    
    channels = []
    channels_result = store.query(get_channels_query)
    index = 0
    for uri, label, comment, logo in channels_result:
        # TODO: get channel logo
        channels.append({"@id" : uri, "rdfs:label" : label.n3(), "rdfs:comment" : comment.n3(), "events" : [], "actions" : [], "parameters" : []})
                
        # get actions
        get_actions_query = """
            PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?action ?label ?comment
            WHERE {
            %s ewe:providesAction ?action .
            ?action rdfs:subClassOf ewe:Action ;
                    rdfs:domain %s;
                    rdfs:label ?label ;
                    rdfs:comment ?comment .
            }
        """ % (uri.n3(), uri.n3())
        actions_result = store.query(get_actions_query)
        action_index = 0

        for action_uri, action_label, action_comment in actions_result:

            channels[index]["actions"].append({"@id" : action_uri, "rdfs:label" : action_label.n3(), "rdfs:comment" : action_comment.n3(), "input_parameters" : [], "output_parameters" : []})

            # get input parameters
            get_input_parameters_query = """
                PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT ?parameter ?label ?comment
                WHERE {
                %s ewe:hasInputParameter ?parameter .
                ?parameter rdfs:subClassOf ewe:Parameter ;
                        rdfs:domain %s;
                        rdfs:label ?label ;
                        rdfs:comment ?comment .
                }
            """ % (action_uri.n3(), uri.n3())

            input_params_result = store.query(get_input_parameters_query)
            for input_param_uri, input_param_label, input_param_comment in input_params_result:
                channels[index]["actions"][action_index]["input_parameters"].append({"@id" : input_param_uri, "rdfs:label" : input_param_label.n3(), "rdfs:comment" : input_param_comment.n3()})

            # get output parameters
            get_output_parameters_query = """
                PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT ?parameter ?label ?comment
                WHERE {
                %s ewe:hasOutputParameter ?parameter .
                ?parameter rdfs:subClassOf ewe:Parameter ;
                        rdfs:domain %s;
                        rdfs:label ?label ;
                        rdfs:comment ?comment .
                }
            """ % (action_uri.n3(), uri.n3())

            output_params_result = store.query(get_output_parameters_query)
            for output_param_uri, output_param_label, output_param_comment in output_params_result:
                channels[index]["actions"][action_index]["output_parameters"].append({"@id" : output_param_uri, "rdfs:label" : output_param_label.n3(), "rdfs:comment" : output_param_comment.n3()})

            action_index+=1
        # get events
        get_events_query = """
            PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?event ?label ?comment
            WHERE {
            %s ewe:generatesEvent ?event .
            ?event rdfs:subClassOf ewe:Event ;
                    rdfs:domain %s;
                    rdfs:label ?label ;
                    rdfs:comment ?comment .
            }
        """ % (uri.n3(), uri.n3())

        event_index = 0
        events_result = store.query(get_events_query)
        for event_uri, event_label, event_comment in events_result:
            channels[index]["events"].append({"@id" : event_uri, "rdfs:label" : event_label.n3(), "rdfs:comment" : event_comment.n3(), "input_parameters" : [], "output_parameters" : []})
            
            # get input parameters
            get_input_parameters_query = """
                PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT ?parameter ?label ?comment
                WHERE {
                %s ewe:hasInputParameter ?parameter .
                ?parameter rdfs:subClassOf ewe:Parameter ;
                        rdfs:domain %s;
                        rdfs:label ?label ;
                        rdfs:comment ?comment .
                }
            """ % (event_uri.n3(), uri.n3())

            input_params_result = store.query(get_input_parameters_query)
            for input_param_uri, input_param_label, input_param_comment in input_params_result:
                channels[index]["events"][event_index]["input_parameters"].append({"@id" : input_param_uri, "rdfs:label" : input_param_label.n3(), "rdfs:comment" : input_param_comment.n3()})

            # get output parameters
            get_output_parameters_query = """
                PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT ?parameter ?label ?comment
                WHERE {
                %s ewe:hasOutputParameter ?parameter .
                ?parameter rdfs:subClassOf ewe:Parameter ;
                        rdfs:domain %s;
                        rdfs:label ?label ;
                        rdfs:comment ?comment .
                }
            """ % (event_uri.n3(), uri.n3())

            output_params_result = store.query(get_output_parameters_query)
            for output_param_uri, output_param_label, output_param_comment in output_params_result:
                channels[index]["events"][event_index]["output_parameters"].append({"@id" : output_param_uri, "rdfs:label" : output_param_label.n3(), "rdfs:comment" : output_param_comment.n3()})

            event_index+=1

        get_parameters_query = """
            PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?parameter ?label ?comment
            WHERE {
            ?parameter rdfs:subClassOf ewe:Parameter ;
                        rdfs:domain %s;
                        rdfs:label ?label ;
                        rdfs:comment ?comment .
            }
        """ % (uri.n3())
        parameters_result = store.query(get_parameters_query)
        for param_uri, param_label, param_comment in parameters_result:
            channels[index]["parameters"].append({"@id" : param_uri, "rdfs:label" : param_label.n3(), "rdfs:comment" : param_comment.n3()})

        index+=1
    #print(channels)
    #print(store.query(rq).serialize(format='json-ld', indent=4))
    return json.dumps(channels)