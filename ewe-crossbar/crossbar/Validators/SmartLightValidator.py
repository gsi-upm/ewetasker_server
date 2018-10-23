import voluptuous
import objectpath, requests
import importlib
from voluptuous import Schema, Required, In, Object, Self, Optional, Exclusive, Inclusive, ALLOW_EXTRA


class SmartLight:
    
    validate = Schema({
    Required('channel'): str, 
    Required('event'): str,
    Required("user"): str,
    Required('params'): {
        Optional("LightPublicIP"): str,
        Optional("LightApiToken"): str,
        Exclusive("LightBrightness", "LightGroup"): int,
        Exclusive("LightColor", "LightGroup"): int,
        Required("LightID"): str,
    },
}, extra=ALLOW_EXTRA)
