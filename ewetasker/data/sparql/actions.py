from rdflib.plugins.stores import sparqlstore

def get_channel_actions(uri_channel):

    #Define the SparQL store
    endpoint = 'http://localhost:3030/ewetasker/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

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
        """ % (uri_channel.n3(), uri_channel.n3())

    actions_result = store.query(get_actions_query)
    store.close()

    return actions_result
    
