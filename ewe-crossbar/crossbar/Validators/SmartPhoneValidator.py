import voluptuous
import objectpath, requests
import importlib
from voluptuous import Schema, Required, In, Object, Self, Optional, Exclusive, Inclusive, ALLOW_EXTRA


class SmartPhone:
    
    validate = Schema({
    Required('channel'): str, 
    Required('event'): str,
    Required("user"): str,
    Required('params'): {
        Exclusive("EventCalendar", "SmartPhoneGroup"): str,
        Exclusive("ToastNotification", "SmartPhoneGroup"): str,
        Exclusive("NavbarNotification", "SmartPhoneGroup"): str,
    },
}, extra=ALLOW_EXTRA)
