import voluptuous
import objectpath, requests
import importlib
from voluptuous import Schema, Required, In, Object, Self, Exclusive, Inclusive, ALLOW_EXTRA


class PresenceSensor:
    
    validate = Schema({
    Required('channel'): str, 
    Required('event'): str,
    Required("user"): str,
    Required('params'): {
        Inclusive("PresenceSensorID", "PresenceSensorGroup"): str,
        Exclusive("PresenceDistance", "PresenceSensorGroup"): float,
        Exclusive("PresenceTime", "PresenceSensorGroup"): str,  
    },
}, extra=ALLOW_EXTRA)
    
