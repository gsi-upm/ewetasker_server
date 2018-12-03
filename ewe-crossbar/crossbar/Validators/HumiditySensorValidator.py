import voluptuous
import objectpath, requests
import importlib
from voluptuous import Schema, Required, In, Object, Self, Optional, Exclusive, Inclusive, ALLOW_EXTRA


class HumiditySensor:
    
    validate = Schema({
    Required('channel'): str, 
    Required('event'): str,
    Required("user"): str,
    Required('params'): {
        Inclusive("HumiditySensorID", "HumiditySensorGroup"): str,
        Exclusive("HumidityLevel", "HumiditySensorGroup"): float,
    },
}, extra=ALLOW_EXTRA)
