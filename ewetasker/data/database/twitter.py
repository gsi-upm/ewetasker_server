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

def get_request_token(username,twitter_username):
    
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    try:
        redirect_url = auth.get_authorization_url()
        log.warning(redirect_url)
        twitter_dict={"oauth_token": auth.request_token["oauth_token"],"user":twitter_username }
        add_user_field(username, "twitter", twitter_dict)
        return '<a href="'+redirect_url+'">Connect with Twitter</a>'
    except tweepy.TweepError:
        log.warning('Error! Failed to get request token.')
        return 'Error! Failed to get request token.'

def set_user_token(oauth_token, oauth_verifier):
    user=get_user_by_field("twitter.oauth_token",oauth_token)
    if (user!=None):
        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.request_token = { 'oauth_token' : oauth_token,
                                'oauth_token_secret' : oauth_verifier }
        try:
            auth.get_access_token(oauth_verifier)
            add_user_field(user["user"], "twitter.access_token", auth.access_token)
            add_user_field(user["user"], "twitter.access_token_secret", auth.access_token_secret)
            log.warning(auth.access_token)
            log.warning(auth.access_token_secret)
            return "Twitter authentication successful"
        except tweepy.TweepError:
            log.warning(tweepy.TweepError)
            return 'Error! Failed to get access token.'
    return 'Error! Failed to get access token, request token not found'
