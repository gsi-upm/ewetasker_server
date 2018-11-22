import json
import os
import tweepy
import logging
from data.database.users import add_user_field, get_user_by_field

log = logging.getLogger('tester.sub')



if os.environ.get('TWITTER_TOKEN') is not None:
    consumer_token = os.environ.get('TWITTER_TOKEN')
    consumer_secret = os.environ.get('TWITTER_SECRET')
else:
    consumer_token = ""
    consumer_secret = ""

def select_twitter_action(action,username):
    log.warning(action["action"])
    if action["action"] not in twitter_functions:
        log.warning("no hay función para twitter")
        return ''
    twitter_functions[action["action"]](username,action["parameters"])
    return ''

def post_tweet(username,parameters):
    user=get_user_by_field("user",username)
    if(user["twitter"]["user"]==parameters["TwitterUsername"]):
        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.set_access_token(user["twitter"]["access_token"], user["twitter"]["access_token_secret"])
        api = tweepy.API(auth)
        api.update_status(parameters["Tweet"])
    else:
        log.warning("Usuarios no coinciden")
    return ''

twitter_functions = {"PostTweet": post_tweet}
