from rdflib.plugins.stores import sparqlstore
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')


def get_input_parameters(actionevent_uri, uri):

    #Define the SparQL store
    endpoint = 'http://' + config['SPARQL']['BASE_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # get input parameters
    get_input_parameters_query = """
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?parameter ?label ?comment ?datatype
        WHERE {
            %s ewe:hasInputParameter ?parameter .
            ?parameter rdfs:subClassOf ewe:Parameter ;
                rdfs:domain %s;
                rdfs:label ?label ;
                rdfs:comment ?comment ;
                rdf:datatype ?datatype .
            }
    """ % (actionevent_uri.n3(), uri.n3())
    
    parameters = store.query(get_input_parameters_query)

    store.close()
    return parameters

def get_output_parameters(actionevent_uri, uri):

    #Define the SparQL store
    endpoint = 'http://' + config['SPARQL']['BASE_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # get input parameters
    get_output_parameters_query = """
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?parameter ?label ?comment ?datatype
        WHERE {
            %s ewe:hasOutputParameter ?parameter .
            ?parameter rdfs:subClassOf ewe:Parameter ;
                rdfs:domain %s;
                rdfs:label ?label ;
                rdfs:comment ?comment ;
                rdf:datatype ?datatype .
            }
    """ % (actionevent_uri.n3(), uri.n3())
    
    parameters = store.query(get_output_parameters_query)

    store.close()
    return parameters

def get_channel_parameters(uri):
    #Define the SparQL store
    endpoint = 'http://' + config['SPARQL']['BASE_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    get_parameters_query = """
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT DISTINCT ?parameter ?label ?comment ?datatype
        WHERE {
  			{ 
    			?action rdfs:subClassOf ewe:Action ;
               			ewe:hasInputParameter ?parameter .
  			}
  			UNION
  			{
                ?event rdfs:subClassOf ewe:Event ;
                        ewe:hasInputParameter ?parameter .
  			}
            ?parameter rdfs:subClassOf ewe:Parameter ;
                rdfs:domain %s;
                rdfs:label ?label ;
                rdfs:comment ?comment ;
                rdf:datatype ?datatype .
        }
    """ % (uri.n3())

    parameters = store.query(get_parameters_query)

    store.close()
    return parameters

def get_custom_channel_parameters(uri):
    #Define the SparQL store
    endpoint = 'http://' + config['SPARQL']['BASE_URL'] + '/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    get_parameters_query = """
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?parameter ?label ?value ?datatype ?baseParameter
        WHERE {
            %s ewe:hasParameter ?parameter .
            ?parameter rdf:type ?baseParameter ;
                        rdf:value ?value .
            ?baseParameter rdfs:label ?label ;
                            rdf:datatype ?datatype .
        }
    """ % (uri.n3())

    parameters = store.query(get_parameters_query)

    store.close()
    return parameters