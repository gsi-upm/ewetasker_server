import json
import os
import logging
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from data.database.users import add_user_field, get_user_by_field
import base64
from email.mime.text import MIMEText
log = logging.getLogger('tester.sub')



if (os.environ.get('GMAIL_CLIENT_ID')!=None)and(os.environ.get('GMAIL_CLIENT_SECRET')!=None):
    client_id=os.environ.get('GMAIL_CLIENT_ID')
    client_secret=os.environ.get('GMAIL_CLIENT_SECRET')
else:
    client_id = ""
    client_secret = ""

def select_gmail_action(action,username):
    log.warning(action["action"])
    if action["action"] not in gmail_functions:
        log.warning("no hay función para gmail")
        return ''
    gmail_functions[action["action"]](username,action["parameters"])
    return ''

def send_message(username,parameters):
    user=get_user_by_field("user",username)
    if(user["gmail"]["user"]==parameters["EmailAddress"]):
        log.warning(user)
        log.warning(client_secret)
        log.warning(client_id)
        credentials=google.oauth2.credentials.Credentials(user["gmail"]["token"],user["gmail"]["refresh_token"],None,user["gmail"]["token_uri"],client_id,client_secret,user["gmail"]["scopes"])
        gmail = build('gmail', 'v1', credentials=credentials)
        message = MIMEText(parameters["EmailMessage"])
        message['to'] = parameters["RecipientAddress"]
        message['from'] = parameters["EmailAddress"]
        message['subject'] = parameters["EmailSubject"]
        message = message.as_string()
        message = base64.urlsafe_b64encode(message.encode('UTF-8')).decode('ascii')
        m = {'raw':message}
        message = (gmail.users().messages().send(userId="me", body=m).execute())
    else:
        log.warning("Usuarios no coinciden")
    return ''

gmail_functions = {"SendEmailMessage": send_message}
