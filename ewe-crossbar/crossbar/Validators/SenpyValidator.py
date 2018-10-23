import voluptuous
import objectpath, requests
import importlib
from voluptuous import Schema, Required, In, Object, Self, Optional, Exclusive, Inclusive, ALLOW_EXTRA


class Senpy:
    
    validate = Schema({
    Required('channel'): str, 
    Required('event'): str,
    Required("user"): str,
    Required('params'): {
        Exclusive("SenpyEmotion", "SenpyGroup"): str,
        Exclusive("SenpySentiment", "SenpyGroup"): str,
    },
}, extra=ALLOW_EXTRA)
