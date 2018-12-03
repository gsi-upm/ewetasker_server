import json
import os
import logging
import base64
import string
import random
import requests
from data.database.users import add_user_field, get_user_by_field
log = logging.getLogger('tester.sub')

client_id=""
client_secret=""
redirect_uri = ""
if (os.environ.get('SPOTIFY_CLIENT_ID')!=None)and(os.environ.get('SPOTIFY_CLIENT_SECRET')!=None)and(os.environ.get('SPOTIFY_REDIRECT_URI')!=None):
    client_id=os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET')
    redirect_uri = "http://"+os.environ.get('API_REDIRECT_URI') + "/connect/spotify"


secrets=""+client_id+":"+client_secret+""
secrets=base64.standard_b64encode(secrets.encode('UTF-8')).decode('ascii')
auth="Basic "+secrets+""

def get_connect_uri(username, service_username):
    scope = 'user-read-playback-state+user-modify-playback-state'
    state=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    authorization_url="https://accounts.spotify.com/authorize?client_id="+client_id+"&response_type=code&redirect_uri="+redirect_uri+"&scope="+scope+"&state="+state+""
    spotify_dict={"user":service_username, "state":state}
    add_user_field(username,"spotify",spotify_dict)
    log.warning(authorization_url)
    return '<a href="'+authorization_url+'">Connect with Spotify</a>'

def set_user_code(code,state):
    user=get_user_by_field("spotify.state",state)
    if (user!=None):
        log.warning("set_user_code")
        uri = "https://accounts.spotify.com/api/token"
        payload = {"grant_type":"authorization_code","code":code,"redirect_uri":redirect_uri} 
        headers = {"Authorization": auth,'Content-Type': 'application/x-www-form-urlencoded'}
        log.warning(redirect_uri)
        response = requests.post(uri, data=payload, headers=headers)
        log.warning(response)
        data=json.loads(response.text)
        log.warning(data)
        spotify_dict={"user":user["spotify"]["user"], "state":state, 
                    "access_token":data["access_token"], "refresh_token":data["refresh_token"]}
        add_user_field(user["user"],"spotify",spotify_dict)
        devices=get_user_devices(user["user"])
        add_user_field(user["user"],"spotify.devices",devices)
        return "Spotify authentication successful, click <a href=http://"+redirect_uri+"/connect/spotify/devices/"+user["spotify"]["user"]+">here</a> to get a list of your available devices."
    return 'Authorization request not set'

def get_user_devices(username):
    user=get_user_by_field("user",username)
    if (user!=None):
        refresh_access_token(user)
        user=get_user_by_field("user",username)
        uri = "https://api.spotify.com/v1/me/player/devices"
        auth="Bearer "+user["spotify"]["access_token"]+""
        headers = {"Accept": "application/json", "Content-Type": "application/json","Authorization": auth}
        response = requests.get(uri, headers=headers)
        data=json.loads(response.text)
        return data
    return None

def get_devices(username):
    devices=get_user_devices(username)
    if devices != None:
        response="Spotify devices:<br/><ul>"
        for device in devices["devices"]:
            response+="<li>Name: "+device["name"]+" Type: "+device["type"]+"</li>"
        response+="</ul>"
        return response
    return "Devices not found"
    
def refresh_access_token(user):
    uri = "https://accounts.spotify.com/api/token"
    payload = {"grant_type":"refresh_token","refresh_token":user["spotify"]["refresh_token"]} 
    headers = {"Authorization": auth,'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(uri, data=payload, headers=headers)
    log.warning(response.text)
    data=json.loads(response.text)
    add_user_field(user["user"],"spotify.access_token",data["access_token"])
