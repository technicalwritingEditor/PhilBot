import os
import json
import Helpers

def SetConfig(id, key, args):
    with open("Data/" + id + "/ServerConfig.json", 'r') as f:
         dir = json.load(f)
    f.close()
  
    #If type is a list we want it to add instead of overwriting
    dir[key] = Helpers.ManageMultipleInput(dir[key], args)

    with open("Data/" + id + "/ServerConfig.json", 'w') as f:
         json.dump(dir, f)
    f.close()

    print(id, "changed config value", key, "to :", dir[key])

def GetConfig(id, key = ""):
     for file in os.listdir("Data"):
          if file == id:
              with open("Data/" + file + "/ServerConfig.json", 'r') as f:
                  if key != "":
                      return json.load(f)[key]
                  else:
                      return json.load(f)
              f.close()