import json
import os
import logging
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from data.database.users import add_user_field, get_user_by_field
log = logging.getLogger('tester.sub')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
client_secret={"web":{"client_id": "",
    "project_id":"ewetasker","auth_uri":"https://accounts.google.com/o/oauth2/auth",
    "token_uri":"https://www.googleapis.com/oauth2/v3/token",
    "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
    "client_secret":""}}
redirect_uri = 'http://'
if (os.environ.get('GMAIL_CLIENT_ID')!=None)and(os.environ.get('GMAIL_CLIENT_SECRET')!=None)and(os.environ.get('GMAIL_REDIRECT_URI')!=None):
    client_secret["web"]["client_id"]=os.environ.get('GMAIL_CLIENT_ID')
    client_secret["web"]["client_secret"]=os.environ.get('GMAIL_CLIENT_SECRET')
    redirect_uri = redirect_uri + os.environ.get('GMAIL_REDIRECT_URI') + "/connect/gmail"

scope=['https://www.googleapis.com/auth/gmail.send']
flow = google_auth_oauthlib.flow.Flow.from_client_config(client_secret,scope)
flow.redirect_uri = redirect_uri
def get_request_uri(username, service_username):
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required.
    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')
    service_username=service_username+"@gmail.com"
    gmail_dict={"state":state,"user":service_username}
    add_user_field(username,"gmail",gmail_dict)
    log.warning(authorization_url)
    return '<a href="'+authorization_url+'">Connect with Gmail</a>'

def set_user_credentials(uri,state):
    user=get_user_by_field("gmail.state",state)
    if (user!=None):
        flow.fetch_token(authorization_response=uri)
        credentials = flow.credentials
        gmail_dict={"state":state,
                    "user":user["gmail"]["user"],
                    "token": credentials.token, 
                    "refresh_token": credentials.refresh_token, 
                    "token_uri": credentials.token_uri,
                    "scopes": credentials.scopes
                    }
        add_user_field(user["user"], "gmail", gmail_dict)
        return "Gmail authentication successful"
    return 'CSRF Warning! State not equal in request and response.'