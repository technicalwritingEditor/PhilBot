import os
import json
import Helpers
import Decorators

data_path = "Data/" + "*id*" + "/ServerConfig.json"
server_config = '''{"MainChannel" : "", "JoinRoles" : [],"StartMessage": "","JoinMessage": "", "AdminPowerBypass" : true, "NoPermissonMessage" : ""}'''
role_config = {"Permissions" : []}
event_config = {"Enabled" : False, "Repeat" : "None", "TimeOfExecution" : {"Year" : 2000, "Month" : 1, "Day" : 1, "Hour" : 0, "Min" : 0, "Second" : 0}, "LastExecuted" : 0, "Target" : "None", "Functions" : []}
command_config = {"Functions" : []}
function_config = {"if": {}, "ifnot": {}}


def config(id, file, args):
    #Making sure args is a list to ensure nothing funky happens.
    if type(args) == tuple:
        args = list(args)

    if type(args) != list:
        args = [args]
   
    #Converting file to proper name and getting their default values
    default_content = {}
    if file == "Server":
        file = "ServerConfig.json"
        default_content = server_config
    if file == "Roles":
        file = "RolesConfig.json" 
    if file == "Event":
        file = "EventConfig.json" 
    if file == "Commands":
        file = "CommandConfig.json"
    if file == "Function":
        file = "FunctionConfig.json" 


    file_path =  "Data/" + id + "/" + file
    if os.path.exists(file_path):
        #Converting args into seperated lists
        ARGS_LISTS = list()
        ARGS_LISTS.append([])
        dot_count = 0
        for arg in args:
            if arg == "/":
               ARGS_LISTS.append([])
               dot_count += 1
            else:
                ARGS_LISTS[dot_count].append(arg)
        #Removing empty lists from argList.
        for arg_list in ARGS_LISTS:
            if len(arg_list) == 0:
                ARGS_LISTS.remove(arg_list)
        #ARGS_LIST Should not be modified after this point.

        #Reading config
        with open(file_path, 'r') as f:
            JSON_file = json.load(f)
        
        #Making changes to specified config 
        if file == "ServerConfig.json":
            if len(ARGS_LISTS) == 2:
                if ARGS_LISTS[0][0] != "AdminPowerBypass": #Should only be able to edit AdminPowerBypas with !powerbypass
                    JSON_file[ARGS_LISTS[0][0]] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]], ARGS_LISTS[1])

        if file == "RolesConfig.json":
            #Adding roles
            if len(ARGS_LISTS) == 1:
                JSON_file = Helpers.manage_multiple_input(JSON_file, ARGS_LISTS[0], role_config)
           
            #Adding perms to roles
            if len(ARGS_LISTS) == 2:
                JSON_file[ARGS_LISTS[0][0]]["Permissions"] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]]["Permissions"], ARGS_LISTS[1], [])
        
        if file == "FunctionConfig.json":
            #Adding function
            if len(ARGS_LISTS) == 1:
                JSON_file = Helpers.manage_multiple_input(JSON_file, ARGS_LISTS[0], function_config)
            #Adding attribute
            if len(ARGS_LISTS) == 2:
                JSON_file[ARGS_LISTS[0][0]] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]], ARGS_LISTS[1], [], function_config)
            #Adding values to attributes or adding blocks to if and ifnot
            if len(ARGS_LISTS) == 3:
                #Adding values to attributes
                if type(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]) == list:
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]], ARGS_LISTS[2], [])
                else:
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]], ARGS_LISTS[2], {})
            
            #Adding attributes to blocks in if and ifnot or setting TimeOfExecution
            if len(ARGS_LISTS) == 4:
                JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]][ARGS_LISTS[2][0]] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]][ARGS_LISTS[2][0]], ARGS_LISTS[3], [])
           
            #Adding values to attributes in blocks in if and ifnot
            if len(ARGS_LISTS) == 5:
                JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]][ARGS_LISTS[2][0]][ARGS_LISTS[3][0]] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]][ARGS_LISTS[2][0]][ARGS_LISTS[3][0]], ARGS_LISTS[4])
       
        if file == "CommandConfig.json":
            #Adding command
            if len(ARGS_LISTS) == 1:
                JSON_file = Helpers.manage_multiple_input(JSON_file, ARGS_LISTS[0], command_config)
            if len(ARGS_LISTS) == 3:
                JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]], ARGS_LISTS[2])

        if file == "EventConfig.json":
            #Adding event
            if len(ARGS_LISTS) == 1:
                JSON_file = Helpers.manage_multiple_input(JSON_file, ARGS_LISTS[0], event_config)

            #Setting values or adding blocks
            if len(ARGS_LISTS) == 3:
                #Making sure user is not editing TimeOfExecution
                if ARGS_LISTS[1][0] != "TimeOfExecution" and ARGS_LISTS[1][0] != "Functions":
                    if type(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]) == list:
                        JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]], ARGS_LISTS[2], [])
                    else:
                        JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]], ARGS_LISTS[2], {})

                #Setting entire TimeOfExecution at once
                if ARGS_LISTS[1][0] == "TimeOfExecution":
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Year"] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Year"], ARGS_LISTS[2][0])
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Month"] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Month"], ARGS_LISTS[2][1])
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Day"] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Day"], ARGS_LISTS[2][2])
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Hour"] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Hour"], ARGS_LISTS[2][3])
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Min"] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Min"], ARGS_LISTS[2][4])
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Second"] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Second"], ARGS_LISTS[2][5])
               
                if ARGS_LISTS[1][0] == "Functions":
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]] = Helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]], ARGS_LISTS[2])
      
        #Writing Changes
        with open(file_path, 'w') as f:
            json.dump(JSON_file, f)
    else: 
        return None

    return JSON_file


def get_config(id, key = ""):
    "Gets config data from Servers(id) ServerConfig. If key is "" then returns full file." 
    for file in os.listdir("Data"):
          if file == id:
              with open("Data/" + file + "/ServerConfig.json", 'r') as f:
                  if key != "":
                      return json.load(f)[key]
                  else:
                      return json.load(f)


@Decorators.read_write_JSON(data_path)
def set_config(id, key, args, JSON_file):
    JSON_file[key] = Helpers.manage_multiple_input(JSON_file[key], args)
    Helpers.print_UTF8(id, "changed config value", key, "to :", JSON_file[key])
    return JSON_file