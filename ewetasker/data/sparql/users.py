from rdflib.plugins.stores import sparqlstore
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')

def create_new_user(username):

    #Define the SparQL store
    endpoint = 'http://' + config['SPARQL']['BASE_URL'] + ':3030/ewetasker/update'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    create_user_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/> 

        INSERT DATA
        {
            ewe:%s rdf:type ewe:User ;
            foaf:accountName '%s'.
        }
    """ % (username, username)
    print(create_user_query)
    users = store.update(create_user_query)
    store.close()

    return ""

def query_user(username):
    #Define the SparQL store
    endpoint = 'http://' + config['SPARQL']['BASE_URL'] + ':3030/ewetasker/query'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Get user
    get_user_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/> 

        SELECT ?user 
        WHERE {
            ?user rdf:type ewe:User;
                foaf:accountName "%s" .
        }
    """ % (username)
    
    user = store.query(get_user_query)
    store.close()
  
    return user

def delete_user(username):
    #Define the SparQL store
    endpoint = 'http://' + config['SPARQL']['BASE_URL'] + ':3030/ewetasker/update'
    store = sparqlstore.SPARQLUpdateStore()
    store.open((endpoint, endpoint))

    # Delete user
    delete_user_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/> 

        DELETE
        {
            ?a ?b ?c ;
  				foaf:accountName ?d .
        }
        WHERE
        {
            ?a ?b ?c ;
                foaf:accountName "%s" .
        }
    """ % (username)
    
    user = store.update(delete_user_query)
    store.close()
  
    return ""