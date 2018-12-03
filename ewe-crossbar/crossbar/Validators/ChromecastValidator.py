import voluptuous
import objectpath, requests
import importlib
from voluptuous import Schema, Required, In, Object, Self, Optional, Exclusive, Inclusive, ALLOW_EXTRA


class Chromecast:
    
    validate = Schema({
    Required('channel'): str, 
    Required('event'): str,
    Required("user"): str,
    Required('params'): {
        Optional("ChromecastLocalIP"): str,
        Optional("ChromecastPublicIP"): str,
        Required("ChromecastVideoUrl"): str,
    },
}, extra=ALLOW_EXTRA)
