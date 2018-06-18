import os
import json
import Helpers
import Decorators

def GetEvents(id):
    with open("Data/" + id + "/EventConfig.json", 'r') as f:
        return json.load(f)

