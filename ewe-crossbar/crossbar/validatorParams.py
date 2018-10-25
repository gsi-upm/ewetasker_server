import voluptuous
import objectpath, requests, sys, os
import importlib
from voluptuous import Schema, Required, In, Exclusive, Inclusive, ALLOW_EXTRA
from twisted.logger import Logger
import time
time.sleep(30)
url = 'http://' + os.environ['API'] + "/channels/base"
log = Logger()
log.info(url)

def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module("Validators."+module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c

data_channels = requests.get(url)
data = data_channels.json()
tree_obj = objectpath.Tree(data)

channels = list(tree_obj.execute("$.channels.*[@['@id']]"))
for i in range(len(channels)):
    channels[i]=channels[i].split('/')[-1]

print(channels)


def verify(params):
    validate(params)
    class_for_name(params["channel"]+"Validator", params["channel"].capitalize()).validate(params)
    

validate = Schema({
    Required('channel'): In(channels), 
    Required('event'): str,
    Required("user"): str
}, extra=ALLOW_EXTRA)


