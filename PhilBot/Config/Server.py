import os
import json
import Helpers
import Decorators

dataPath = "Data/" + "*id*" + "/ServerConfig.json"
@Decorators.ReadWriteJson(dataPath)
def SetConfig(id, key, args, jsonFile):
    jsonFile[key] = Helpers.ManageMultipleInput(jsonFile[key], args)
    print(id, "changed config value", key, "to :", jsonFile[key])
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
              f.close()