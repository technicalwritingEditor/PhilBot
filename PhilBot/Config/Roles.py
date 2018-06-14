import os
import json
import Helpers
import Decorators

roleConfig = {"Permissions" : []}

dataPath = "Data/" + "*id*" + "/RolesConfig.json"

def GetRole(id, key = "", subKey = ""):
    "Gets the role from server. If no subKey is specified returns full role. If no key is specified returns all roles"
    with open("Data/" + id + "/RolesConfig.json", 'r') as f:
        dic = json.load(f)
    f.close()
    if key != "":
        if subKey == "":
            return dic[key]
        else:
            return dic[key][subKey]
    else:
        return dic