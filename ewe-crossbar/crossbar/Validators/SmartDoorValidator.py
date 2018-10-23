import voluptuous
import objectpath, requests
import importlib
from voluptuous import Schema, Required, In, Object, Self, Optional, Exclusive, Inclusive, ALLOW_EXTRA


class SmartDoor:
    
    validate = Schema({
    Required('channel'): str, 
    Required('event'): str,
    Required("user"): str,
    Required('params'): {
        Optional("DoorLocalIP"): str,
        Optional("DoorPublicIP"): str,
        Required("DoorID"): str,
    },
}, extra=ALLOW_EXTRA)
