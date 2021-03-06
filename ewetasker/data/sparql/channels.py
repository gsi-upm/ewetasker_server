from rdflib.plugins.stores import sparqlstore
import time
import os

def get_all_base_channels():

    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Get channels
    get_channels_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>

        SELECT ?channel ?label ?comment ?logo ?color
        WHERE {
            ?channel rdfs:subClassOf ewe:Channel ;
                    rdfs:label ?label ;
                    foaf:logo ?logo ;
                    rdfs:comment ?comment ;
                    dbo:colour ?color .
        
        }
    """
    
    channels = store.query(get_channels_query)
    store.close()
    return channels

def get_all_custom_channels():
    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Get channels
    get_channels_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>

        SELECT ?channel ?label ?comment ?baseChannel ?logo ?color
        WHERE {
            ?baseChannel rdfs:subClassOf ewe:Channel ;
                    dbo:colour ?color ;
                    foaf:logo ?logo .
            ?channel rdf:type ?baseChannel ;
                    rdfs:label ?label ;
                    rdfs:comment ?comment .
        
        }
    """
    
    channels = store.query(get_channels_query)
    store.close()
    return channels

def get_all_custom_category_channels(category_uri):
    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Get channels
    get_channels_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>

        SELECT ?channel ?label ?comment ?baseChannel ?logo ?color
        WHERE {
            ?baseChannel rdfs:subClassOf ewe:Channel ;
                    foaf:logo ?logo ;
                    dbo:colour ?color ;
                    ewe:hasCategory <%s> .
            ?channel rdf:type ?baseChannel ;
                    rdfs:label ?label ;
                    rdfs:comment ?comment .
        
        }
    """ % (category_uri)
    
    channels = store.query(get_channels_query)
    store.close()
    return channels

def get_all_category_channels(category_uri):
    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Get channels
    get_channels_query = """
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>

        SELECT ?channel ?label ?comment ?logo ?color
        WHERE {
            ?channel rdfs:subClassOf ewe:Channel ;
                rdfs:label ?label ;
                rdfs:comment ?comment ;
                foaf:logo ?logo ;
                dbo:colour ?color ;
                ewe:hasCategory <%s> .
        }
    """ % (category_uri)
    
    channels = store.query(get_channels_query)
    store.close()
    return channels

def get_all_subchannels(channel_uri):
    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Get channels
    get_channels_query = """
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT ?channel ?label ?comment
        WHERE {
            ?channel rdf:type <%s>;
                rdfs:label ?label ;
                rdfs:comment ?comment .
        }
    """ % (channel_uri)
    
    channels = store.query(get_channels_query)
    store.close()
    return channels


def create_channel(base, name, c_type, label, comment, parameters):

    timestamp = str(int(round(time.time())))
    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/update'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    triples = ""
    # Create parameters
    for param in parameters:
        triples = triples + """
            ewe:%s rdf:type <%s> ;
                    rdf:value '%s' .
            <%s%s> ewe:hasParameter <%s%s> .
        """ % (param["rdfs:label"].replace(" ", "").lower() + timestamp, param["rdf:type"], param["rdf:value"], base, name + timestamp, base, param["rdfs:label"].replace(" ", "").lower() + timestamp)
    # Create channel
    get_channels_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        INSERT DATA
        {
            ewe:%s rdf:type <%s> ;
                rdfs:label '%s';
                rdfs:comment '%s'.
            %s
        }
    """ % (name + timestamp, c_type, label, comment, triples)

    channels = store.update(get_channels_query)
    store.close()

    return ""

def create_channel_with_triples(triples):
    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/update'
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

    channels = store.update(get_channels_query)
    store.close()

    return ""

def delete_custom_channel(uri):

    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/update'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Delete channel and parameters
    delete_channels_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        DELETE
        {
            <%s> ?b ?c .
            ?param ?d ?e
        }
        WHERE
        {
            <%s> ?b ?c;
                ewe:hasParameter ?param .
            ?param ?d ?e
        }
    """ % (uri, uri)
    channels = store.update(delete_channels_query)
        # Delete channel
    delete_channels_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        DELETE
        {
            <%s> ?b ?c .
        }
        WHERE
        {
            <%s> ?b ?c.
        }
    """ % (uri, uri)

    channels = store.update(delete_channels_query)
    store.close()

    return ""


def get_channel_by_action(action_uri):
    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    action_uri = action_uri[40:]
    # Get channels
    get_channel_query = """
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>

        SELECT ?uri ?label ?logo ?comment ?color
        WHERE {
            ?uri rdfs:subClassOf ewe:Channel ;
                rdfs:label ?label ;
                foaf:logo ?logo ;
                dbo:colour ?color ;
                ewe:providesAction  ewe:%s ;
                rdfs:comment ?comment .
        
        }
    """ % (action_uri)
    
    channel = store.query(get_channel_query)
    store.close()
    return channel
    

def get_channel_by_event(event_uri):
    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    event_uri = event_uri[40:]
    # Get channels
    get_channel_query = """
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>

        SELECT ?uri ?label ?logo ?comment ?color
        WHERE {
            ?uri rdfs:subClassOf ewe:Channel ;
                rdfs:label ?label ;
                foaf:logo ?logo ;
                dbo:colour ?color ;
                ewe:generatesEvent  ewe:%s ;
                rdfs:comment ?comment .
        
        }
    """ % (event_uri)
    
    channel = store.query(get_channel_query)
    store.close()
    return channel

def get_channel_colour(color_uri):

    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Get color
    get_color_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>


        SELECT ?color
        WHERE {
            dbo:%s a dbo:Colour ;
				dbo:colourHexCode ?color .
        }
    """% (color_uri.split("/")[-1])
    
    color = store.query(get_color_query)
    store.close()
    return color