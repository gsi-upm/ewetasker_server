from rdflib.plugins.stores import sparqlstore


def get_input_parameters(actionevent_uri, uri):

    #Define the SparQL store
    endpoint = 'http://localhost:3030/ewetasker/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

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
    """ % (actionevent_uri.n3(), uri.n3())
    
    parameters = store.query(get_input_parameters_query)

    store.close()
    return parameters

def get_output_parameters(actionevent_uri, uri):

    #Define the SparQL store
    endpoint = 'http://localhost:3030/ewetasker/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # get input parameters
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
    """ % (actionevent_uri.n3(), uri.n3())
    
    parameters = store.query(get_output_parameters_query)

    store.close()
    return parameters

def get_channel_parameters(uri):
    #Define the SparQL store
    endpoint = 'http://localhost:3030/ewetasker/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

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

    parameters = store.query(get_parameters_query)

    store.close()
    return parameters

