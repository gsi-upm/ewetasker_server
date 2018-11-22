from data.database.twitter import get_request_token, set_user_token
from data.database.gmail import get_request_uri, set_user_credentials
import json
import logging
log = logging.getLogger('tester.sub')

service_functions = {"twitter": get_request_token, "gmail":get_request_uri}
def select_service(service, username, service_username):
    if service not in service_functions:
        log.warning("no hay integración con ese servicio")
    else:
        return service_functions[service](username, service_username)
    return 'No integration available with '+service+''

def auth_twitter(oauth_token, oauth_verifier):
    log.warning(oauth_token)
    log.warning(oauth_verifier)
    return set_user_token(oauth_token, oauth_verifier)

def auth_gmail(uri,state):
    return set_user_credentials(uri,state)
