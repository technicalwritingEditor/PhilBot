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


