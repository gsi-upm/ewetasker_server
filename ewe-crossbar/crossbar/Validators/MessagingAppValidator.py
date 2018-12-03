import voluptuous
import objectpath, requests
import importlib
from voluptuous import Schema, Required, In, Object, Self, Optional, Exclusive, Inclusive, ALLOW_EXTRA


class MessagingApp:
    
    validate = Schema({
    Required('channel'): str, 
    Required('event'): str,
    Required("user"): str,
    Required('params'): {
        Required("MessagingAppUserID"): str,
        Required("MessagingAppMessage"): str,
    },
}, extra=ALLOW_EXTRA)
