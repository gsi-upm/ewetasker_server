from data.database.twitter import get_request_token, set_user_token
import json
import logging
log = logging.getLogger('tester.sub')

service_functions = {"twitter": get_request_token}
def select_service(service, username):
    if service not in service_functions:
        log.warning("no hay integración con ese servicio")
    else:
        return service_functions[service](username)
    return 'No integration available with '+service+''

def auth_twitter(oauth_token, oauth_verifier):
    return set_user_token(oauth_token, oauth_verifier)
