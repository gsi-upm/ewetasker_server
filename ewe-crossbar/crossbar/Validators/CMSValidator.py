import voluptuous
import objectpath, requests
import importlib
from voluptuous import Schema, Required, In, Object, Self, Optional, Exclusive, Inclusive, ALLOW_EXTRA


class CMS:
    
    validate = Schema({
    Required('channel'): str, 
    Required('event'): str,
    Required("user"): str,
    Required('params'): {
        Required("ContentID"): str,
    },
}, extra=ALLOW_EXTRA)
