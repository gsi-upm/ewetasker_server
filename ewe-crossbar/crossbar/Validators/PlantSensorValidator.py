import voluptuous
import objectpath, requests
import importlib
from voluptuous import Schema, Required, In, Object, Self, Optional, Exclusive, Inclusive, ALLOW_EXTRA


class PlantSensor:
    
    validate = Schema({
    Required('channel'): str, 
    Required('event'): str,
    Required("user"): str,
    Required('params'): {
        Inclusive("PlantSensorID", "PlantSensorGroup"): str,
        Exclusive("PlantMoisture", "PlantSensorGroup"): float,
        Exclusive("PlantLight", "PlantSensorGroup"): float,
        Exclusive("PlantTemperature", "PlantSensorGroup"): float,
        Exclusive("PlantConductivity", "PlantSensorGroup"): float,
    },
}, extra=ALLOW_EXTRA)
