import os
import json
import Helpers

def SetConfig(id, key, args):
    with open("Data/" + id + "/ServerConfig.json", 'r') as f:
         dir = json.load(f)
    f.close()
  
    #If type is a list we want it to add instead of overwriting
    if(type(dir[key]) == list):
       for object in args:
           print(object)
           if object in dir[key]:
               dir[key].remove(object)
           else:
               dir[key].append(object)
    else:
        dir[key] = Helpers.ToString(args)

    with open("Data/" + id + "/ServerConfig.json", 'w') as f:
         json.dump(dir, f)
    f.close()

    print(id, "changed config ", key, ":", dir[key])

def GetConfig(id, key):
     for file in os.listdir("Data"):
          if file == id:
              with open("Data/" + file + "/ServerConfig.json", 'r') as f:
                  return json.load(f)[key]
              f.close()
