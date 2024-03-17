import json

def get_key(key):
    return json.load(open("botstate.json"))[key]

def set_key(key, value):
    state = json.load(open("botstate.json"))
    state[key] = value
    json.dump(state,open("botstate.json","w"),indent=2)