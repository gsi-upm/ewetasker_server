from rdflib.plugins.stores import sparqlstore
import time
import logging
import os


def create_new_rule(label, comment, events, actions, user_uri):

    timestamp = str(int(round(time.time())))
    
    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/update'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Event triples
    event_triples = ""
    event_ids = ""
    event_counter = 1
    for event in events:

        # Event
        event_triples += "?event%d rdf:type <%s>; rdf:type ewe:Event; rdfs:domain <%s>. " % (event_counter, event["@id"], event["rdfs:domain"])
        event_ids += "ewe:triggeredBy <%s> ; " % (event["@id"])
        # Param
        param_triples = ""
        param_counter = 1
        for param in event["parameters"]:
            param_triples += "?event%d ewe:hasParameter ?eparam%d. ?eparam%d rdf:type <%s> . ?eparam%d!rdf:value <%s> '%s' . " % (event_counter, param_counter, param_counter, param["rdf:type"], param_counter, param["ewe:operation"], param["rdf:value"])
            param_counter += 1
        event_counter +=1
        event_triples += param_triples
    
    # Action triples
    action_triples = ""
    action_ids = ""
    action_counter = 1
    for action in actions:

        # Action
        action_triples += "ewe:action_%s%d rdf:type <%s>;  rdf:type ewe:Action; rdfs:domain <%s>. " % (action["rdfs:label"].replace(" ", "").lower(), action_counter, action["@id"], action["rdfs:domain"])
        action_ids += "ewe:executes <%s> ; " % (action["@id"])
        # Param
        param_triples = ""
        param_counter = 1
        for param in action["parameters"]:
            print(param)
            """
            if param["output"]:
                param_triples += "ewe:action_%s%d ewe:hasParameter <%s>. <%s>  rdf:value '%s' . " % (action["rdfs:label"].replace(" ", "").lower(), action_counter, param["@id"], param["@id"], param["rdf:value"])
            else:
                param_triples += "ewe:action_%s%d ewe:hasParameter ewe:%s%d. ewe:%s%d rdf:type <%s> . ewe:%s%d  rdf:value '%s' . " % (action["rdfs:label"].replace(" ", "").lower(), action_counter, param["rdfs:label"].replace(" ", "").lower(), param_counter, param["rdfs:label"].replace(" ", "").lower(), param_counter, param["rdf:type"], param["rdfs:label"].replace(" ", "").lower(), param_counter, param["rdf:value"])             
            """
            param_triples += "ewe:action_%s%d ewe:hasParameter ewe:%s%d. ewe:%s%d rdf:type <%s> . ewe:%s%d  rdf:value '%s' . " % (action["rdfs:label"].replace(" ", "").lower(), action_counter, param["rdfs:label"].replace(" ", "").lower(), param_counter, param["rdfs:label"].replace(" ", "").lower(), param_counter, param["rdf:type"], param["rdfs:label"].replace(" ", "").lower(), param_counter, param["rdf:value"])             
            param_counter += 1
        
        action_counter += 1 
        action_triples += param_triples
    
    rule = "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>. @prefix ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>. @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>. @prefix string: <http://www.w3.org/2000/10/swap/string#>. @prefix math: <http://www.w3.org/2000/10/swap/math#>. { %s } => { %s }." % (event_triples, action_triples)

    create_rule_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX string: <http://www.w3.org/2000/10/swap/string#>
        PREFIX math: <http://www.w3.org/2000/10/swap/math#>

        INSERT DATA
        {
            ewe:%s rdf:type ewe:Rule ;
                rdfs:label '%s';
                rdfs:comment '%s';
                rdf:value "%s";
                %s
                %s
                ewe:hasCreator '%s'.
        
        }
    """ % (label.replace(" ", "").lower() + timestamp, label, comment, rule, event_ids, action_ids, user_uri)
    rules = store.update(create_rule_query)
    store.close()

    return ""

def get_all_user_rules(user_uri):

    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Get rules
    get_rules_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX string: <http://www.w3.org/2000/10/swap/string#>
        PREFIX math: <http://www.w3.org/2000/10/swap/math#>

        SELECT ?uri
        WHERE {
            ?uri rdf:type ewe:Rule ;
  				ewe:hasCreator '%s' .
        }
    """ % (user_uri)
    
    rules = store.query(get_rules_query)
    store.close()
    return rules

def get_rule_by_uri(rule_uri):
    
        #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))
    rule_uri = rule_uri.split("/")[-1]
    get_rule_query = """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX string: <http://www.w3.org/2000/10/swap/string#>
                PREFIX math: <http://www.w3.org/2000/10/swap/math#>

                SELECT ?label ?comment ?event ?action ?rule
                WHERE {
                    ewe:%s rdf:type ewe:Rule ;
                        rdfs:label ?label ;
                        rdfs:comment ?comment ;
                        ewe:triggeredBy ?event ;
                        ewe:executes ?action ;
                        rdf:value ?rule .
                }
    """ % (rule_uri)
    rule_query = store.query(get_rule_query)

    store.close()
    return rule_query

def delete_rule(uri):

    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/update'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Delete channel and parameters
    delete_rule_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX string: <http://www.w3.org/2000/10/swap/string#>
        PREFIX math: <http://www.w3.org/2000/10/swap/math#>

        DELETE
        {
            <%s> ?b ?c .
        }
        WHERE
        {
            <%s> ?b ?c .
        }
    """ % (uri, uri)

    rule = store.update(delete_rule_query)
    store.close()

    return ""