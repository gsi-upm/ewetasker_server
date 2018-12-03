import voluptuous
import objectpath, requests
import importlib
from voluptuous import Schema, Required, In, Object, Self, Optional, Exclusive, Inclusive, ALLOW_EXTRA


class TemperatureSensor:
    
    validate = Schema({
    Required('channel'): str, 
    Required('event'): str,
    Required("user"): str,
    Required('params'): {
        Optional("Degrees"): int,
        Required("TemperatureSensorID"): str,
    },
}, extra=ALLOW_EXTRA)
