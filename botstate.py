# main imports
import json
import os

# local imports
import util

def get_key(key):
    return json.load(open(os.path.join(util.LOC,"botstate.json")))[key]

def set_key(key, value):
    state = json.load(open(os.path.join(util.LOC,"botstate.json")))
    state[key] = value
    json.dump(state,open(os.path.join(util.LOC,"botstate.json"),"w"),indent=2)