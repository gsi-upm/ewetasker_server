import json
import os
import logging
import base64
import requests
from data.database.users import add_user_field, get_user_by_field
from data.database.spotify import get_user_devices
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

def select_spotify_action(action,username):
    log.warning(action["action"])
    if action["action"] not in spotify_functions:
        log.warning("no hay función para gmail")
        return ''
    spotify_functions[action["action"]](username,action["parameters"])
    return ''

def play(username,parameters):
    user=get_user_by_field("user",username)
    if (user!=None):
        devices=get_user_devices(user["user"])
        add_user_field(user["user"],"spotify.devices",devices)
        if(devices["devices"][0]["name"]==parameters["MusicPlayerName"]):
            uri = "https://api.spotify.com/v1/me/player/play?device_id="+devices["devices"][0]["id"]
            auth="Bearer "+user["spotify"]["access_token"]+""
            song=getSong(parameters["Song"], parameters["Artist"], parameters["Album"], user["spotify"]["access_token"])
            payload={"uris":[song]}
            headers = {"Accept": "application/json", "Content-Type": "application/json","Authorization": auth}
            response = requests.put(uri, data=payload, headers=headers)
            log.warning(response.text)
        else:
            log.warning("Usuarios no coinciden")
    return ''

def getSong(song, artist, album, access_token):
    song=song.replace(" ", "%20")
    artist=artist.replace(" ", "%20")
    album=album.replace(" ", "%20")
    uri = "https://api.spotify.com/v1/search?q="+artist+"%20"+album+"%20"+song+"&type=track&market=ES&limit=1&offset=5"
    auth="Bearer "+access_token+""
    headers = {"Accept": "application/json", "Content-Type": "application/json","Authorization": auth}
    response = requests.get(uri, headers=headers)
    tracks=json.loads(response.text)
    return tracks["tracks"]["items"][0]["uri"]

spotify_functions = {"PlaySong": play}
