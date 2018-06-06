import os
import json
import Helpers

#commandConfig contains a list of Functions each with a list of attributes.
functionConfig = []
commandConfig = {"Functions" : {}}
    
def AddCommand(id, args):
    "Adds role to id(server)s RolesConfig"
    #Reading roles config file.
    with open("Data/" + id + "/CommandConfig.json", 'r') as f:
        dic = json.load(f)
    f.close()
    
    for arg in args:
        if arg in dic:
            dic.pop(arg)
        else:
            dic[arg] = commandConfig

    #Setting Role config file.
    with open("Data/" + id + "/CommandConfig.json", 'w') as f:
        json.dump(dic, f)
    print(id, "Command Config was changed to", dic)

def AddFunctions(id, command, args):
    #Reading roles config file.
    with open("Data/" + id + "/CommandConfig.json", 'r') as f:
        dic = json.load(f)
    f.close()
 
    for arg in args:
        if arg in dic[command]["Functions"]:
            dic[command]["Functions"].pop(arg)
        else:
            dic[command]["Functions"][arg] = functionConfig
    
    with open("Data/" + id + "/CommandConfig.json", 'w') as f:
       json.dump(dic, f)
    f.close()
    print(id, "Command Config was changed to", dic)

def GetCommandFunctions(id, command):
    "Gets commands function from server(id)"
    with open("Data/" + id + "/CommandConfig.json", 'r') as f:
        dic = json.load(f)
    f.close()
    return dic[command]["Functions"]

def GetCommands(id):
    "Gets commands from server(id)"
    with open("Data/" + id + "/CommandConfig.json", 'r') as f:
        dic = json.load(f)
    f.close()
    return dic

def SetCommandFunctionsAttributes(id, command, attribute, args):
    "Gets commands function from server(id)"
    with open("Data/" + id + "/CommandConfig.json", 'r') as f:
        dic = json.load(f)
    f.close()
    
    dic[command]["Functions"][attribute] = Helpers.ManageMultipleInput(dic[command]["Functions"][attribute], args)

    with open("Data/" + id + "/CommandConfig.json", 'w') as f:
       json.dump(dic, f)
    f.close()
    print(id, "Command Config was changed to", dic)

def GetCommandFunctionsAttributes(id, command, function):
    with open("Data/" + id + "/CommandConfig.json", 'r') as f:
        dic = json.load(f)
    f.close()
    return dic[command]["Functions"][function]
