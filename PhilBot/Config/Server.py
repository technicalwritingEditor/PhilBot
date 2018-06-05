import os
import json
import Helpers

def SetConfig(id, key, args):
    with open("Data/" + id + "/ServerConfig.json", 'r') as f:
         dir = json.load(f)
    f.close()
    
    #Making sure args is a list to insure nothing funky happens.
    if type(args) == tuple:
        args = list(args)
    if type(args) == str:
        args = [args]
    if type(args) == bool:
        args = [args]

    #Converting string bool to bool type.
    if type(dir[key]) == bool:
        if args[0] == "true" or args[0] == True:
            args[0] = True
        if args[0] == "false" or args[0] == False:
            args[0] = False
    
    #Checking if key and args types match.
    isMatch = False
    if type(dir[key]) == list:
        isMatch = type(args[0]) == str
    else: 
        isMatch = type(args[0]) == type(dir[key])
    
    if isMatch:
       #If type is a list we want it to add instead of overwriting    
       if type(args[0]) == str:
           dir[key] = Helpers.ManageMultipleInput(dir[key], args)
       else:
           dir[key] = args[0]
      
       with open("Data/" + id + "/ServerConfig.json", 'w') as f:
           json.dump(dir, f)
       f.close()

       print(id, "changed config value", key, "to :", dir[key])

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