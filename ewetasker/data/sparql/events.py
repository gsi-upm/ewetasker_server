from rdflib.plugins.stores import sparqlstore
import os

def get_channel_events(uri_channel):

    #Define the SparQL store
    endpoint = 'http://' + os.environ['SPARQL_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

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
    """ % (uri_channel.n3(), uri_channel.n3())

    events_result = store.query(get_events_query)

    store.close()

    return events_result
    
