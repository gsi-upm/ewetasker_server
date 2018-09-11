from rdflib.plugins.stores import sparqlstore
import time
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')

def create_new_rule(label, comment, events, actions, username):

    timestamp = str(int(round(time.time())))
    
    #Define the SparQL store
    endpoint = 'http://' + config['SPARQL']['BASE_URL'] + ':3030/ewetasker/update'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Event triples
    event_triples = ""
    event_counter = 1
    for event in events:

        # Event
        event_triples += "?event%d rdf:type <%s>. " % (event_counter, event["@id"])

        # Param
        param_triples = ""
        param_counter = 1
        for param in event["parameters"]:
            param_triples += "?event%d ewe:hasParameter ?eparam%d. ?eparam%d rdf:type <%s> . ?eparam%d!rdf:value %s '%s' . " % (event_counter, param_counter, param_counter, param["rdf:type"], param_counter, param["operation"], param["rdf:value"])
            param_counter += 1
        
        event_triples += param_triples
    
    # Action triples
    action_triples = ""
    action_counter = 1
    for action in actions:

        # Action
        action_triples += "ewe:action_%s%d rdf:type <%s>. " % (action["rdfs:label"].replace(" ", "").lower(), action_counter, action["@id"])

        # Param
        param_triples = ""
        param_counter = 1
        for param in action["parameters"]:
            print(param)
            if param["output"]:
                param_triples += "ewe:action_%s%d ewe:hasParameter <%s>. <%s>  rdf:value '%s' . " % (action["rdfs:label"].replace(" ", "").lower(), action_counter, param["@id"], param["@id"], param["rdf:value"])
            else:
                param_triples += "ewe:action_%s%d ewe:hasParameter ewe:%s%d. ewe:%s%d rdf:type <%s> . ewe:%s%d  rdf:value '%s' . " % (action["rdfs:label"].replace(" ", "").lower(), action_counter, param["rdfs:label"].replace(" ", "").lower(), param_counter, param["rdfs:label"].replace(" ", "").lower(), param_counter, param["rdf:type"], param["rdfs:label"].replace(" ", "").lower(), param_counter, param["rdf:value"])             
            param_counter += 1

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
            ewe:hasCreator '%s'.
        
        }
    """ % (label.replace(" ", "").lower() + timestamp, label, comment, rule, username)
    print(create_rule_query)
    rules = store.update(create_rule_query)
    store.close()

    return ""