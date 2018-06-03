from rdflib.plugins.stores import sparqlstore
import time
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')

def get_all_base_channels():

    #Define the SparQL store
    endpoint = 'http://' + config['SPARQL']['BASE_URL'] + ':3030/ewetasker/query'
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
                    foaf:logo ?logo ;
                    rdfs:comment ?comment .
        
        }
    """
    
    channels = store.query(get_channels_query)
    store.close()
    return channels

def get_all_custom_channels():
    #Define the SparQL store
    endpoint = 'http://' + config['SPARQL']['BASE_URL'] + ':3030/ewetasker/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Get channels
    get_channels_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>


        SELECT ?channel ?label ?comment ?baseChannel ?logo
        WHERE {
            ?baseChannel rdfs:subClassOf ewe:Channel ;
                    foaf:logo ?logo .
            ?channel rdf:type ?baseChannel ;
                    rdfs:label ?label ;
                    rdfs:comment ?comment .
        
        }
    """
    
    channels = store.query(get_channels_query)
    store.close()
    return channels


def create_channel(base, name, c_type, label, comment, parameters):

    timestamp = str(round(time.time()*1000))
    #Define the SparQL store
    endpoint = 'http://' + config['SPARQL']['BASE_URL'] + ':3030/ewetasker/update'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    triples = ""
    # Create parameters
    for param in parameters:
        triples = triples + """
            <%s%s> rdf:type <%s> ;
                    rdf:value '%s' .
            <%s%s> ewe:hasParameter <%s%s> .
        """ % (base, param["rdfs:label"].replace(" ", "").lower() + timestamp, param["rdf:type"], param["rdf:value"], base, name + timestamp, base, param["rdfs:label"].replace(" ", "").lower() + timestamp)
    # Create channel
    get_channels_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        INSERT DATA
        {
            <%s%s> rdf:type <%s> ;
                rdfs:label '%s';
                rdfs:comment '%s'.
            %s
        }
    """ % (base, name + timestamp, c_type, label, comment, triples)

    channels = store.update(get_channels_query)
    store.close()

    return ""

def create_channel_with_triples(triples):
    #Define the SparQL store
    endpoint = 'http://' + config['SPARQL']['BASE_URL'] + ':3030/ewetasker/update'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    triples_query = ""
    for s, p, o in triples:
        triples_query = triples_query + s.n3() + p.n3() + o.n3() + "."
    # Create channel
    get_channels_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        INSERT DATA
        {
            %s
        }
    """ % (triples_query)
    print(get_channels_query)
    channels = store.update(get_channels_query)
    store.close()

    return ""