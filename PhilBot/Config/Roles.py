import os
import json
import Helpers

roleConfig = {"PermissionLevel" : 0, "Permissions" : []}

def SetRole(id, args):
    "Adds role to id(server)s RolesConfig"
    #Reading roles config file.
    with open("Data/" + id + "/RolesConfig.json", 'r') as f:
        dic = json.load(f)
    f.close()
    
    for arg in args:
        if arg in dic:
            dic.pop(arg)
        else:
            dic[arg] = roleConfig

    #Setting Role config file.
    with open("Data/" + id + "/RolesConfig.json", 'w') as f:
        json.dump(dic, f)
    print(id, "RolesConfig was changed to", dic)

def SetPermissons(id, key, args):   
    "Sets role(key) from server(id) to args"
    #Reading roles config file.
    with open("Data/" + id + "/RolesConfig.json", 'r') as f:
        dic = json.load(f)
    f.close()
  
    #Setting values
    try:
        dic[key]["PermissionLevel"] = int(args[0])
        print(id, "changed role config ", key, "PermissionLevel", ":", dic[key]["PermissionLevel"])
    except:
        dic[key]["Permissions"] = Helpers.ManageMultipleInput(dic[key]["Permissions"], args)
        print(id, "changed role config ", key, "Permissions", ":", dic[key]["Permissions"])
   
    #Setting Role config file.
    with open("Data/" + id + "/RolesConfig.json", 'w') as f:
        json.dump(dic, f)

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