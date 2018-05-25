from rdflib.plugins.stores import sparqlstore

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
    
    channels = store.query(get_channels_query)
    store.close()
    return channels