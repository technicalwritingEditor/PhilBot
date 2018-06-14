import os
import json
import Helpers
import Decorators

dataPath = "Data/" + "*id*" + "/ServerConfig.json"
serverConfig = '''{"MainChannel" : "", "JoinRoles" : [],"StartMessage": "","JoinMessage": "", "AdminPowerBypass" : true, "NoPermissonMessage" : ""}'''
roleConfig = {"Permissions" : []}
commandConfig = {"if": {}, "ifnot": {}}


def Config(id, file, args):
    #Making sure args is a list to ensure nothing funky happens.
    if type(args) == tuple:
        args = list(args)

    if type(args) != list:
        args = [args]
   
    #Converting file to proper name and getting their default values
    defaultContent = {}
    if file == "Server":
        file = "ServerConfig.json"
        defaultContent = serverConfig
    if file == "Roles":
        file = "RolesConfig.json" 
    if file == "Events":
        file = "EventConfig.json" 
    if file == "Commands":
        file = "CommandConfig.json" 


    filePath =  "Data/" + id + "/" + file
    if os.path.exists(filePath):
        #Converting args into seperated lists
        argsLists = list()
        argsLists.append([])
        dotCount = 0
        for arg in args:
            if arg == "/":
               argsLists.append([])
               dotCount += 1
            else:
                argsLists[dotCount].append(arg)
        #Removing empty lists from argList.
        for argList in argsLists:
            if len(argList) == 0:
                argsLists.remove(argList)

        #Reading config
        with open(filePath, 'r') as f:
            jsonFile = json.load(f)
        
        #Making changes to specified config 
        if file == "ServerConfig.json":
            if len(argsLists) == 2:
                jsonFile[argsLists[0][0]] = Helpers.ManageMultipleInput(jsonFile[argsLists[0][0]], argsLists[1])

        if file == "RolesConfig.json":
            #Adding roles
            if len(argsLists) == 1:
                jsonFile = Helpers.ManageMultipleInput(jsonFile, argsLists[0], roleConfig)
           
            #Adding perms to roles
            if len(argsLists) == 2:
                jsonFile[argsLists[0][0]]["Permissions"] = Helpers.ManageMultipleInput(jsonFile[argsLists[0][0]]["Permissions"], argsLists[1], [])

        if file == "CommandConfig.json":
            #Adding command
            if len(argsLists) == 1:
                jsonFile = Helpers.ManageMultipleInput(jsonFile, argsLists[0], commandConfig)
            #Adding attribute
            if len(argsLists) == 2:
                jsonFile[argsLists[0][0]] = Helpers.ManageMultipleInput(jsonFile[argsLists[0][0]], argsLists[1], [], commandConfig)
             #Adding attribute
            if len(argsLists) == 3:
                jsonFile[argsLists[0][0]][argsLists[1][0]] = Helpers.ManageMultipleInput(jsonFile[argsLists[0][0]][argsLists[1][0]], argsLists[2], [])
            #Adding attributes to if and ifnot
            if len(argsLists) == 4:
                jsonFile[argsLists[0][0]][argsLists[1][0]][argsLists[2][0]] = Helpers.ManageMultipleInput(jsonFile[argsLists[0][0]][argsLists[1][0]][argsLists[2][0]], argsLists[3], [])

        #Writing Changes
        with open(filePath, 'w') as f:
            json.dump(jsonFile, f)
    else: 
        return None

    return jsonFile

def GetConfig(id, key = ""):
    "Gets config data from Servers(id) ServerConfig. If key is "" then returns full file." 
    for file in os.listdir("Data"):
          if file == id:
              with open("Data/" + file + "/ServerConfig.json", 'r') as f:
                  if key != "":
                      return json.load(f)[key]
                  else:
                      return json.load(f)

@Decorators.ReadWriteJson(dataPath)
def SetConfig(id, key, args, jsonFile):
    jsonFile[key] = Helpers.ManageMultipleInput(jsonFile[key], args)
    print(id, "changed config value", key, "to :", jsonFile[key])
    return jsonFile