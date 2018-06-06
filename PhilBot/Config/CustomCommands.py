import os
import json
import Helpers
import Decorators

#commandConfig contains a list of Functions each with a list of attributes.
functionConfig = []
commandConfig = {"Functions" : {}}

@Decorators.ReadWriteJson("Data/" + "*id*" + "/CommandConfig.json")    
def AddCommand(id, args, jsonFile):
    "Adds role to id(server)s RolesConfig."

    jsonFile = Helpers.ManageMultipleInput(jsonFile, args, commandConfig)
    print(id, "Command Config was changed to", jsonFile)
    return jsonFile

@Decorators.ReadWriteJson("Data/" + "*id*" + "/CommandConfig.json")    
def AddFunctions(id, command, args, jsonFile):
    "Adds functions to command."
   
    jsonFile[command]["Functions"] = Helpers.ManageMultipleInput(jsonFile[command]["Functions"], args, functionConfig)
    print(id, "Command Config was changed to", jsonFile)
    return jsonFile

@Decorators.ReadWriteJson("Data/" + "*id*" + "/CommandConfig.json")    
def SetFunctionAttributes(id, command, attribute, args, jsonFile):
    "Adds attributes to functions."
   
    jsonFile[command]["Functions"][attribute] = Helpers.ManageMultipleInput(jsonFile[command]["Functions"][attribute], args)
    print(id, "Command Config was changed to", jsonFile)
    return jsonFile

def GetCommands(id):
    "Gets commands from server(id)."

    with open("Data/" + id + "/CommandConfig.json", 'r') as f:
        dic = json.load(f)
    f.close()
    return dic

def GetFunctions(id, command):
    "Gets commands function from server(id)."

    with open("Data/" + id + "/CommandConfig.json", 'r') as f:
        dic = json.load(f)
    f.close()
    return dic[command]["Functions"]


def GetAttributes(id, command, function):
    with open("Data/" + id + "/CommandConfig.json", 'r') as f:
        dic = json.load(f)
    f.close()
    return dic[command]["Functions"][function]
