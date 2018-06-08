import os
import json
import Helpers
import Decorators
#Conditions for ifAttribute
containsRoles = []
hasPermisson = []

#Attribute
sayAttribute = []
addRolesAttribute = []

functionConfig = {}
commandConfig = {"if": {}, "ifnot": {}}

dataPath = "Data/" + "*id*" + "/CommandConfig.json"

@Decorators.ReadWriteJson(dataPath)    
def SetCommand(id, args, jsonFile):
    "Adds role to id(server)s RolesConfig."

    jsonFile = Helpers.ManageMultipleInput(jsonFile, args, commandConfig)
    print(id, "Command Config was changed to", jsonFile)
    return jsonFile

@Decorators.ReadWriteJson(dataPath)    
def SetAttribute(id, command, args, jsonFile):
    "Adds role to id(server)s RolesConfig."

    jsonFile[command] = Helpers.ManageMultipleInput(jsonFile[command], args, [])
    print(id, "Command Config was changed to", jsonFile)
    return jsonFile

@Decorators.ReadWriteJson(dataPath)    
def SetAttributeValue(id, command, attribute, args, jsonFile):
    jsonFile[command][attribute] = Helpers.ManageMultipleInput(jsonFile[command][attribute], args)
    print(id, "Command Config was changed to", jsonFile)
    return jsonFile

@Decorators.ReadWriteJson(dataPath)    
def SetBlock(id, command, type, args, jsonFile):
    if type == "if" or type == "ifnot": 
        jsonFile[command][type] = Helpers.ManageMultipleInput(jsonFile[command][type], args, {})
    print(id, "Command Config was changed to", jsonFile)
    return jsonFile

@Decorators.ReadWriteJson(dataPath)    
def SetBlockAttribute(id, command, type, block, args, jsonFile):
    jsonFile[command][type][block] = Helpers.ManageMultipleInput(jsonFile[command][type][block], args, [])
    print(id, "Command Config was changed to", jsonFile)
    return jsonFile

@Decorators.ReadWriteJson(dataPath)    
def SetBlockAttributeValue(id, command, type, block, condition, args, jsonFile):
    jsonFile[command][type][block][condition] = Helpers.ManageMultipleInput(jsonFile[command][type][block][condition], args)
    print(id, "Command Config was changed to", jsonFile)
    return jsonFile

def GetCommand(id, command):
     with open("Data/" + id + "/CommandConfig.json", 'r') as f:
        jsonFile = json.load(f)
     f.close()
     return jsonFile[command]

def GetCommands(id):
    "Gets CommandConig for server(id)."
    with open("Data/" + id + "/CommandConfig.json", 'r') as f:
        jsonFile = json.load(f)
    f.close()
    return jsonFile


