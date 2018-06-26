import asyncio
import os
from Config import Server, Roles
import json
import shutil
import inspect
import discord

server_config = {"MainChannel" : "", "JoinRoles" : [],"StartMessage": "","JoinMessage": "", "AdminPowerBypass" : True, "NoPermissonMessage" : ""}


def get_default_config(server = None):
    "Returns a dictionary of default server config values."
    dict = server_config
    
    #To find the default value of MainChannel program first 
    #checks if there is any text channel named general, if not just picks first channel in text_channel_list.
    #This of course can only happen if server is specified.
    if server != None:
        text_channel_list = []
        for channel in server.channels:
            if str(channel.type) == "text":
                text_channel_list.append(channel.id)
                if channel.name == "general":
                    dict["MainChannel"] = channel.id
        if dict["MainChannel"] == "" and len(text_channel_list) > 0:
            dict["MainChannel"] = text_channel_list[0]

    dict["JoinMessage"] = "**Welcome @ to the server!**"
    dict["StartMessage"] = "**This bot has restarted.**"
    dict["NoPermissonMessage"] = "**You do not have permisson to do that.**"
    dict["AdminPowerBypass"] = True
    
    return dict


def set_default_config_values(server):
     "Sets server's ServerConfig.json to default values."

     default_config = get_default_config(server)
     Server.set_config(server.id, "MainChannel", default_config["MainChannel"])
     Server.set_config(server.id, "JoinMessage", default_config["JoinMessage"])
     Server.set_config(server.id, "StartMessage", default_config["StartMessage"])
     Server.set_config(server.id, "NoPermissonMessage", default_config["NoPermissonMessage"])
     Server.set_config(server.id, "AdminPowerBypass", default_config["AdminPowerBypass"])


def update_config_keys(server):
    "Updates ServerConfig.json keys to match server_configs keys."
    
    with open("Data/" + server.id + "/ServerConfig.json", 'r') as f:
        JSON_file = json.load(f)
   
    new_JSON_file = dict(JSON_file)
    for key in server_config:
        if key not in JSON_file:
            new_JSON_file[key] = get_default_config(server)[key]
            print("Adding key:", key, "to", server.id)

    for key in JSON_file:
        if key not in server_config:
            del new_JSON_file[key]
            print("Removing key:", key, "from", server.id)
        
    with open("Data/" + server.id + "/ServerConfig.json", 'w') as f:
        json.dump(new_JSON_file, f)



def check_data_integrity(bot):
    "Checks and fixes the file integrity of Data.\nA.K.A Replaces files which are currupt, missing, ETC."

    for server in bot.servers:
        server_path = "Data/" + server.id

        #This is for the main server folder.
        if not os.path.exists(server_path):
            os.makedirs(server_path)
        #And this is for the json files contained within.
        check_json(server_path + "/RolesConfig.json", {})
        check_json(server_path + "/CommandConfig.json", {})
        check_json(server_path + "/EventConfig.json", {})
        check_json(server_path + "/FunctionConfig.json", {})
        if check_json(server_path + "/ServerConfig.json", server_config):
            set_default_config_values(server)
        
        update_config_keys(server)
        remove_absent_servers(bot)


def remove_absent_servers(bot):
    "Removes server's data files which the bot is no longer connected to."
    
    for file in os.listdir("Data"):
        delete_file = True;
        for server in bot.servers:
            if(server.id == file):
                delete_file = False
        if delete_file:
            shutil.rmtree("Data/" + file)


def manage_multiple_input(origin, args, dict_value = None, dict_content = {}):
    """Removes or adds args to origin, then returns the modifed version.\n
      
       origin: is the variable you're trying to edit. It can be a list, dict, str, int or bool.\n

       args: is the aguments you're tring to add to origin. It can be a str, bool, int or list/tuple of str\n

       dict_value: is what ever value you want to assign to keys added to a dict. It can be anything.\n

       dict_content: is what ever value you want to assign to keys added to a dict. It can be anything."""
       
    #Ensuring args is list to make coding easier.
    if type(args) == bool:
        if args == True:
            args = ["true"]
        if args == False:
            args = ["false"]
    if type(args) == str:
        args = [args]
    if type(args) == int:
        args = [str(args)]
    if type(args) == tuple:
        args = list(args)

    #Each if stament below is handling for a different origin type.
    if type(origin) == list:
       for arg in args:
           if arg in origin:
               origin.remove(arg)
           else:
               origin.append(arg)

    if type(origin) == dict:
        for arg in args:
            #This is to make sure you're not removing a variable which is supposed to be permanent.
            if arg not in dict_content:
                if arg in origin:
                    del origin[arg]
                else:
                    origin[arg] = dict_value

    if type(origin) == str:
        if type(args) != str:
            origin = " ".join(args)
        else:
            origin = args

    if type(origin) == int:
        if type(args) != str:
            origin = int(" ".join(args))
        else:
            origin = int(args)
    if type(origin) == bool:
        if args[0] == "true":
            origin = True
        if args[0] == "false":
            origin = False
    return origin


def check_json(path, default_JSON_Code):
    "Checks if specified Json file can't be read or dosen't exists and recreates it.\nReturns true if JSON file was replaced."
   
    #Deletes JSON if it's invalid so it can be recreated.
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                config = json.load(f) #Returns an exception if f is an invalid json file, thus except is executed.
                if config == None:
                    os.remove(path)
    except:
        os.remove(path)
        
    #Creates new JSON if it's missing
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump(default_JSON_Code, f)
        return True
    else:
        return False


def check_permisson(bot, command_name, member):
    "Checks if user has permission for command(commandName)."

    if Server.get_config(member.server.id, "AdminPowerBypass"):
        if member.server.get_channel(Server.get_config(member.server.id, "MainChannel")).permissions_for(member).administrator: 
            return True
   
    has_perm = False
    for role in member.roles:
        if role.name in Roles.get_role(member.server.id):
            if command_name in Roles.get_role(server.id, role.name,"Permissions"):
                has_perm = True
    return has_perm  


async def give_roles(bot, member, args):
    "Adds/removes roles specifed in args to member."

    member_roles = member.roles
    for role_name in args:
        role = discord.utils.get(member.server.roles, name = role_name)
        if role in member_roles:
            member_roles.remove(role)
        else:
            member_roles.append(role)
    await bot.replace_roles(member, *member_roles)


def has_roles(bot, member, args):
    "Returns true if member has all roles specified in args."

    does_have_roles = True;
    for role in args:
       roleData = discord.utils.get(member.server.roles, name = role)
       if roleData not in member.roles:
           does_have_roles = False
    return does_have_roles


def get_config(serverID, config):
    with open("Data/" + str(serverID) + "/" + config, 'r') as f:
        return json.load(f)


def format_JSON(header, JSON_Code, indent = "|  "):
    "Takes in a json serializable object and converts it to a more readable format"
    
    INDENT_AMOUNT = "|  "
    formated_JSON = header + ":\n"
    if type(JSON_Code) == list:
        i = 0
        for value in JSON_Code:
            i += 1
            if type(value) == list or type(value) == dict:
                formated_JSON += indent + format_JSON(header, value, indent + INDENT_AMOUNT)
            else:
                formated_JSON += indent + "#" + str(i) + " " + str(value) + "\n"      
    if type(JSON_Code) == dict:
        for key in JSON_Code:
            if type(JSON_Code[key]) == list or type(JSON_Code[key]) == dict:
                formated_JSON += indent + format_JSON(key, JSON_Code[key], indent + INDENT_AMOUNT)
            else:
                formated_JSON += indent + key + " : " + str(JSON_Code[key]) + "\n"

    return str(formated_JSON)

