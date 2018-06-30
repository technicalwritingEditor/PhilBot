import os
import json
import helpers

#Config files paths.
bot_config = "BotConfig.json"
server_config = "Data/*id*/ServerConfig.json"
event_config = "Data/*id*/EventConfig.json"
function_config = "Data/*id*/FunctionConfig.json"
command_config = "Data/*id*/CommandConfig.json"
role_config = "Data/*id*/RolesConfig.json"
user_config = "Data/*id*/UserConfig.json"

role_config_content = {"Permissions" : [], "GodMode" : False}
user_config_content = {"Permissions" : [], "GodMode" : False}
event_config_content = {"Enabled" : False, "Repeat" : "None", "TimeOfExecution" : {"Year" : 2000, "Month" : 1, "Day" : 1, "Hour" : 0, "Min" : 0, "Second" : 0}, "LastExecuted" : 0, "Target" : "None", "Functions" : []}
command_config_content = {"Functions" : []}
function_config_content = {"if": {}, "ifnot": {}}



def get_config(config_path, server_id = ""):
    if server_id != "":
        config_path = convert_data_path(server_id, config_path)
    with open(config_path, 'r') as f:
         return json.load(f)

def set_config(id, file, args):
    #Making sure args is a list to ensure nothing funky happens.
    if type(args) == str:
        args = args.split()
    if type(args) == tuple:
        args = list(args)
    if type(args) != list:
        args = [args]

    #Converting file to proper name and getting their default values
    if file == "Users":
        file = "UserConfig.json"
    if file == "Server":
        file = "ServerConfig.json"
    if file == "Roles":
        file = "RolesConfig.json" 
    if file == "Events": 
        file = "EventConfig.json" 
    if file == "Commands":
        file = "CommandConfig.json"
    if file == "Functions":
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
        if file == "UserConfig.json":
            if len(ARGS_LISTS) == 1:
                JSON_file = helpers.manage_multiple_input(JSON_file, ARGS_LISTS[0], user_config_content)
            if len(ARGS_LISTS) == 3:
               JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]], ARGS_LISTS[2])

        if file == "ServerConfig.json":
            if len(ARGS_LISTS) == 2:
                JSON_file[ARGS_LISTS[0][0]] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]], ARGS_LISTS[1])

        if file == "RolesConfig.json":
            #Adding roles
            if len(ARGS_LISTS) == 1:
                JSON_file = helpers.manage_multiple_input(JSON_file, ARGS_LISTS[0], role_config_content)
           
            if len(ARGS_LISTS) == 3:
                JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]], ARGS_LISTS[2])
        
        if file == "FunctionConfig.json":
            #Adding function
            if len(ARGS_LISTS) == 1:
                JSON_file = helpers.manage_multiple_input(JSON_file, ARGS_LISTS[0], function_config_content)
            #Adding attribute
            if len(ARGS_LISTS) == 2:
                JSON_file[ARGS_LISTS[0][0]] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]], ARGS_LISTS[1], [], function_config_content)
            #Adding values to attributes or adding blocks to if and ifnot
            if len(ARGS_LISTS) == 3:
                #Adding values to attributes
                if type(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]) == list:
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]], ARGS_LISTS[2], [])
                else:
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]], ARGS_LISTS[2], {})
            
            #Adding attributes to blocks in if and ifnot or setting TimeOfExecution
            if len(ARGS_LISTS) == 4:
                JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]][ARGS_LISTS[2][0]] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]][ARGS_LISTS[2][0]], ARGS_LISTS[3], [])
           
            #Adding values to attributes in blocks in if and ifnot
            if len(ARGS_LISTS) == 5:
                JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]][ARGS_LISTS[2][0]][ARGS_LISTS[3][0]] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]][ARGS_LISTS[2][0]][ARGS_LISTS[3][0]], ARGS_LISTS[4])
       
        if file == "CommandConfig.json":
            #Adding command
            if len(ARGS_LISTS) == 1:
                JSON_file = helpers.manage_multiple_input(JSON_file, ARGS_LISTS[0], command_config_content)
            if len(ARGS_LISTS) == 3:
                JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]], ARGS_LISTS[2])

        if file == "EventConfig.json":
            #Adding event
            if len(ARGS_LISTS) == 1:
                JSON_file = helpers.manage_multiple_input(JSON_file, ARGS_LISTS[0], event_config_content)

            #Setting values or adding blocks
            if len(ARGS_LISTS) == 3:
                #Making sure user is not editing TimeOfExecution
                if ARGS_LISTS[1][0] != "TimeOfExecution" and ARGS_LISTS[1][0] != "Functions":
                    if type(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]) == list:
                        JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]], ARGS_LISTS[2], [])
                    else:
                        JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]], ARGS_LISTS[2], {})

                #Setting entire TimeOfExecution at once
                if ARGS_LISTS[1][0] == "TimeOfExecution":
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Year"] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Year"], ARGS_LISTS[2][0])
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Month"] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Month"], ARGS_LISTS[2][1])
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Day"] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Day"], ARGS_LISTS[2][2])
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Hour"] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Hour"], ARGS_LISTS[2][3])
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Min"] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Min"], ARGS_LISTS[2][4])
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Second"] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]]["Second"], ARGS_LISTS[2][5])
               
                if ARGS_LISTS[1][0] == "Functions":
                    JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]] = helpers.manage_multiple_input(JSON_file[ARGS_LISTS[0][0]][ARGS_LISTS[1][0]], ARGS_LISTS[2])
      
        #Writing Changes
        with open(file_path, 'w') as f:
            json.dump(JSON_file, f)
    else: 
        return None

    return JSON_file


def convert_data_path(server_id, config_path):
     return config_path.replace("*id*", server_id)




