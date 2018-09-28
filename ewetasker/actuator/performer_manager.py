import json
import logging
from actuator.performers.chromecast import select_chromecast_action

channels_functions = {"Chromecast": select_chromecast_action}
log = logging.getLogger('tester.sub')
#log.warning('warning test')

def select_performer(actions_json):
    actions_json = json.loads(actions_json)
    if (actions_json["success"]==0):
        log.warning("no hay acciones")
        return ''
    for action in actions_json["actions"]:
        if action["channel"] not in channels_functions:
            log.warning("no hay performer")
            continue
        channels_functions[action["channel"]](action)
    return ''