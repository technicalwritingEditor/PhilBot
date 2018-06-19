import asyncio
import os
from Config import Server, Roles
import json
import shutil
import inspect
import discord

server_config = '''{"MainChannel" : "", "JoinRoles" : [],"StartMessage": "","JoinMessage": "", "AdminPowerBypass" : true, "NoPermissonMessage" : ""}'''

def to_string(args):
    "Converts iterables of strings to a single string."
    string = ""
    if type(args) != str:
        for arg in args:
            if string == "":
                string += arg
            else:
                string +=  " " + arg
    else:
        string = args
    return string


def get_default_config(server = None):
    "Returns a dictionary of default server config values."
    dic = json.loads(server_config)
    
    if server:
        #Getting default channel
        text_channel_list = []
        for channel in server.channels:
            if str(channel.type) == "text":
                text_channel_list.append(channel)
                    
                if(channel.name == "general"):
                    selected_channel = channel
        if selected_channel.name != "general":
            selected_channel = text_channel_list[len(text_channel_list) - 1]

        dic["MainChannel"] = selected_channel.id + ""
  
    dic["JoinMessage"] = "**Welcome @ to the server!**"
    dic["StartMessage"] = "**This bot has restarted.**"
    dic["NoPermissonMessage"] = "**You do not have permisson to do that.**"
    dic["AdminPowerBypass"] = True
    
    return dic


def set_default_config_values(server):
     "Sets server's ServerConfig.json to default values."

     #Setting default values
     Server.set_config(server.id, "MainChannel", get_default_config(server)["MainChannel"])
     Server.set_config(server.id, "JoinMessage", get_default_config()["JoinMessage"])
     Server.set_config(server.id, "StartMessage", get_default_config()["StartMessage"])
     Server.set_config(server.id, "NoPermissonMessage", get_default_config()["NoPermissonMessage"])
     Server.set_config(server.id, "AdminPowerBypass", get_default_config()["AdminPowerBypass"])


def update_config_keys(server):
    "Adds & removes keys from server's ServerConfig.json to match default serverConfig."
    
    #Updating serverJson with newest keys
    with open("Data/" + server.id + "/ServerConfig.json", 'r') as f:
        dir = json.load(f)
    
    #Adding new keys
    default_server_config = json.loads(server_config)
    for key in default_server_config:
        if key not in dir:
            dir[key] = default_server_config[key]
            dir[key] = get_default_config()[key]
            print("Adding key:", key, "to", server.id)

    #Removing old keys
    remove_keys = []
    for key in dir:
        if key not in default_server_config:
            remove_keys.append(key)
            print("Removing key:", key, "from", server.id)
    for key in remove_keys:
        dir.pop(key)
        
    with open("Data/" + server.id + "/ServerConfig.json", 'w') as f:
        json.dump(dir, f)



def check_file_integrity(bot):
    "Checks and fixes the file integrity of Data"

    for server in bot.servers:
        server_path = "Data/" + server.id
        
        #Checking for files
        if not os.path.exists(server_path):
            os.makedirs(server_path)
        check_json(server_path + "/RolesConfig.json", "{}")
        check_json(server_path + "/CommandConfig.json", "{}")
        check_json(server_path + "/EventConfig.json", "{}")

        if check_json(server_path + "/ServerConfig.json", server_config):
            set_default_config_values(server)
        
        update_config_keys(server)
        remove_absent_servers(bot)


def remove_absent_servers(bot):
    for file in os.listdir("Data"):
        delete_file = True;
        for server in bot.servers:
            if(server.id == file):
                delete_file = False
        if delete_file:
            shutil.rmtree("Data/" + file)


def manage_multiple_input(origin, args, dict_default = None, dict_content = {}):
    "Removes or adds args to origin."
    if type(origin) == list:
       for arg in args:
           if arg in origin:
               origin.remove(arg)
           else:
               origin.append(arg)

    if type(origin) == dict:
        for arg in args:
            #This is to make sure user is not removing any default values.
            if arg not in dict_content:
                if arg in origin:
                    origin.pop(arg)
                else:
                    origin[arg] = dict_default

    if type(origin) == str:
        origin = to_string(args)
    if type(origin) == int:
        origin = int(to_string(args))
  
    if type(origin) == bool:
        if type(args) != list:
            args = [args]
        if args[0] == "true":
            origin = True
        if args[0] == "false":
            origin = False

    return origin


def check_json(path, default_JSON_Code):
    """Checks if specified Json file can't be read or dosn't exists and recreates it."""
   
    #Deleting Jason if it's invalid so it can be recreated.
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                config = json.load(f)
                if config == None:
                    os.remove(path)
    except:
        os.remove(path)
        
    #Creates new Jason if it's missing
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write(default_JSON_Code)
        return True
    else:
        return False


def check_permisson(bot, command_name, message):
    "Checks if user has permission for command(commandName)."
   
    if Server.get_config(message.server.id, "AdminPowerBypass"):
        if message.channel.permissions_for(message.author).administrator: return True
   
    has_perm = False
    for role in message.author.roles:
        if role.name in Roles.get_role(message.server.id):
            if command_name in Roles.get_role(message.server.id, role.name,"Permissions"):
                has_perm = True
    return has_perm  


async def give_roles(bot, member, args):
    #Adds/removes roles in servers StartRoles config to member.
    member_roles = member.roles
    for role in args:
        roleData = discord.utils.get(member.server.roles, name = role)
        if roleData in member_roles:
            member_roles.remove(roleData)
        else:
            member_roles.append(roleData)

    await bot.replace_roles(member, *member_roles)


def has_roles(bot, member, args):
    has_all_roles = True;
    for role in args:
       roleData = discord.utils.get(member.server.roles, name = role)
       if roleData not in member.roles:
           has_all_roles = False
    return has_all_roles