import os
import json
import Helpers
import Decorators

def get_events(id):
    with open("Data/" + id + "/EventConfig.json", 'r') as f:
        return json.load(f)

