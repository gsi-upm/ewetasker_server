import voluptuous
import objectpath, requests
import importlib
from voluptuous import Schema, Required, In, Object, Self, Optional, Exclusive, Inclusive, ALLOW_EXTRA


class SmartTv:
    
    validate = Schema({
    Required('channel'): str, 
    Required('event'): str,
    Required("user"): str,
    Required('params'): {
        Optional("TvLocalIP"): str,
        Optional("TvPublicIP"): str,
        Optional("TvImage"): str,
    },
}, extra=ALLOW_EXTRA)
