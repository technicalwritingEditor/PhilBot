import os
import json
import Helpers
import Decorators

roleConfig = {"Permissions" : []}

@Decorators.ReadWriteJson("Data/" + "*id*" + "/RolesConfig.json")
def SetRole(id, args, jsonFile):
    "Adds role to id(server)s RolesConfig"
    
    jsonFile = Helpers.ManageMultipleInput(jsonFile, args, roleConfig)
    print(id, "RolesConfig was changed to", jsonFile)
    return jsonFile

@Decorators.ReadWriteJson("Data/" + "*id*" + "/RolesConfig.json")
def SetPermissons(id, key, args, jsonFile):   
    "Sets role(key) from server(id) to args"

    jsonFile[key]["Permissions"] = Helpers.ManageMultipleInput(jsonFile[key]["Permissions"], args)
    return jsonFile

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