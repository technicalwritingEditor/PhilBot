import os
import json
import Helpers
import Decorators

data_path = "Data/" + "*id*" + "/RolesConfig.json"


def get_role(id, key = "", subKey = ""):
    "Gets the role from server. If no subKey is specified returns full role. If no key is specified returns all roles"
    with open("Data/" + id + "/RolesConfig.json", 'r') as f:
        dict = json.load(f)
    f.close()
    if key != "":
        if subKey == "":
            return dict[key]
        else:
            return dict[key][subKey]
    else:
        return dict