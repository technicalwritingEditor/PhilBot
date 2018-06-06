import asyncio
import os
from Config import Server, Roles
import json
import shutil
import inspect
import discord

serverConfig = '''{"MainChannel" : "", "JoinRoles" : [],"StartMessage": "","JoinMessage": "", "AdminPowerBypass" : true, "NoPermissonMessage" : ""}'''

rolesConfig = '''{}'''
commandConfig = '''{}'''

def ToString(args):
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

def GetDefaultConfig(server = None):
    "Returns a dictionary of default server config values."
    dic = json.loads(serverConfig)
    
    if server:
        #Getting default channel
        textChannelList = []
        for channel in server.channels:
            if str(channel.type) == "text":
                textChannelList.append(channel)
                    
                if(channel.name == "general"):
                    selectedChannel = channel
        if selectedChannel.name != "general":
            selectedChannel = textChannelList[len(textChannelList) - 1]

        dic["MainChannel"] = selectedChannel.id + ""
  
    dic["JoinMessage"] = "**Welcome @ to the server!**"
    dic["StartMessage"] = "**This bot has restarted.**"
    dic["NoPermissonMessage"] = "**You do not have permisson to do that.**"
    dic["AdminPowerBypass"] = True
    
    return dic

def SetDefaultConfigValues(server):
     "Sets server's ServerConfig.json to default values."

     #Setting default values
     Server.SetConfig(server.id, "MainChannel", GetDefaultConfig(server)["MainChannel"])
     Server.SetConfig(server.id, "JoinMessage", GetDefaultConfig()["JoinMessage"])
     Server.SetConfig(server.id, "StartMessage", GetDefaultConfig()["StartMessage"])
     Server.SetConfig(server.id, "NoPermissonMessage", GetDefaultConfig()["NoPermissonMessage"])
     Server.SetConfig(server.id, "AdminPowerBypass", GetDefaultConfig()["AdminPowerBypass"])

def UpdateConfigKeys(server):
    "Adds & removes keys from server's ServerConfig.json to match default serverConfig."
    
    #Updating serverJson with newest keys
    with open("Data/" + server.id + "/ServerConfig.json", 'r') as f:
        dir = json.load(f)
    f.close()
    
    #Adding new keys
    defaultServerConfig = json.loads(serverConfig)
    for key in defaultServerConfig:
        if key not in dir:
            dir[key] = defaultServerConfig[key]
            dir[key] = GetDefaultConfig()[key]
            print("Adding key:", key, "to", server.id)

    #Removing old keys
    removeKeys = []
    for key in dir:
        if key not in defaultServerConfig:
            removeKeys.append(key)
            print("Removing key:", key, "from", server.id)
    for key in removeKeys:
        dir.pop(key)
        
    with open("Data/" + server.id + "/ServerConfig.json", 'w') as f:
        json.dump(dir, f)


async def CheckFileIntegrity(bot):
    "Checks and fixes the file integrity of Data"
   
    emptyServerConfig = json.loads(serverConfig)
    for server in bot.servers:
        serverPath = "Data/" + server.id
        
        #Checking for files
        if not os.path.exists(serverPath):
            os.makedirs(serverPath)
        CheckJson(serverPath + "/RolesConfig.json", rolesConfig)
        CheckJson(serverPath + "/CommandConfig.json", commandConfig)

        if CheckJson(serverPath + "/ServerConfig.json", serverConfig):
            SetDefaultConfigValues(server)
        
        UpdateConfigKeys(server)
    
    #Removing missing servers from Data
    for file in os.listdir("Data"):
        deleteFile = True;
        for server in bot.servers:
            if(server.id == file):
                deleteFile = False
        if deleteFile:
            shutil.rmtree("Data/" + file)

def ManageMultipleInput(origin, args, dictDefault = None):
    "Removes or adds args to origin."
    if type(origin) == list:
       for object in args:
           if object in origin:
               origin.remove(object)
           else:
               origin.append(object)

    if type(origin) == dict:
        for arg in args:
            if arg in origin:
                origin.pop(arg)
            else:
                origin[arg] = dictDefault

    if type(origin) == str:
        origin = ToString(args)
   
    if type(origin) == bool:
        if type(args) != list:
            args = [args]
        
        if args[0] == "true":
            origin = True
        if args[0] == "false":
            origin = False

    return origin

def CheckJson(path, defaultJsonCode):
    """Checks if specified Json file can't be read or dosn't exists and recreates it."""
   
    #Deleting Jason if it's invalid so it can be recreated.
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                config = json.load(f)
                if config == None:
                    os.remove(path)
            f.close()
    except:
        os.remove(path)
        
    #Creates new Jason if it's missing
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write(defaultJsonCode)
        f.close()
        return True
    else:
        return False

def CheckPermisson(bot, commandName, message):
    "Checks if user has permission for command(commandName)."
   
    if Server.GetConfig(message.server.id, "AdminPowerBypass"):
        if message.channel.permissions_for(message.author).administrator: return True
   
    hasPerm = False
    for role in message.author.roles:
        if role.name in Roles.GetRole(message.server.id):
            if commandName in Roles.GetRole(message.server.id, role.name,"Permissions"):
                hasPerm = True
    return hasPerm  

async def GiveRoles(bot, member, args):
    #Adds/removes roles in servers StartRoles config to member.
    memberRoles = member.roles
    for role in args:
        roleData = discord.utils.get(member.server.roles, name = role)
        if roleData in memberRoles:
            memberRoles.remove(roleData)
        else:
            memberRoles.append(roleData)

    await bot.replace_roles(member, *memberRoles)