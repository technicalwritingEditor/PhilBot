import asyncio
import os
from Config import Server, Roles
import json
import shutil
import inspect

serverConfig = '''{"MainChannel" : "", "JoinRoles" : [],"StartMessage": "","JoinMessage": "", "AdminPowerBypass" : true}'''

rolesConfig = '''{}'''

def ToString(args):
    "Converts iterables of strings to a single string"
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

async def UpdateData(bot, sendStartMessage = False):
    "Getting a new version of serverConfig to compare with server instance for updating"
    emptyServerConfig = json.loads(serverConfig)
    
    """Updates Data files"""
    for server in bot.servers:
        serverPath = "Data/" + server.id
        
        #Create server directory
        if not os.path.exists(serverPath):
            os.makedirs(serverPath)
       
        #ServerConfig
        if CheckJson(serverPath + "/ServerConfig.json", serverConfig):
            #Getting a list of channels in server to select the top or select general 
            textChannelList = []
            for channel in server.channels:
                if str(channel.type) == "text":
                    textChannelList.append(channel)
                    
                    if(channel.name == "general"):
                        selectedChannel = channel
            if selectedChannel.name != "general":
                selectedChannel = textChannelList[len(textChannelList) - 1]

            #Setting default values
            Server.SetConfig(server.id, "MainChannel", selectedChannel.id + "")
            Server.SetConfig(server.id, "JoinMessage", "**Welcome @ to the server!**")
            Server.SetConfig(server.id, "StartMessage", "**This bot has restarted**")
        
        #Updating serverJson with newest keys
        with open("Data/" + server.id + "/ServerConfig.json", 'r') as f:
               dir = json.load(f)
        f.close()
        
        #Adding new keys
        for key in emptyServerConfig:
            if key not in dir:
                dir[key] = emptyServerConfig[key]
                print("Adding key:", key, "to", server.id)
        #Removing old keys
        removeKeys = []
        for key in dir:
            if key not in emptyServerConfig:
                removeKeys.append(key)
                print("Removing key:", key, "from", server.id)
        for key in removeKeys:
            dir.pop(key)
        
        with open("Data/" + server.id + "/ServerConfig.json", 'w') as f:
            json.dump(dir, f)

        #RolesConfig
        CheckJson(serverPath + "/RolesConfig.json", rolesConfig)

        #Announce bot 
        if sendStartMessage: 
            await bot.send_message(server.get_channel(Server.GetConfig(server.id, "MainChannel")), Server.GetConfig(server.id,"StartMessage"))
    
    #Removing missing servers from Data
    for file in os.listdir("Data"):
        deleteFile = True;
        for server in bot.servers:
            if(server.id == file):
                deleteFile = False
        if deleteFile:
            shutil.rmtree("Data/" + file)

def ManageMultipleInput(origin, args):
    "Removes or adds args to origin. **FOR LIST**"
    if(type(origin) == list):
       for object in args:
           if object in origin:
               origin.remove(object)
           else:
               origin.append(object)
    else:
        origin = ToString(args)
    return origin

def CheckJson(path, defaultJsonCode):
    """Checks if specified Json file can't be read or dosn't exists and recreates it"""
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

def CheckPermisson(commandName, ctx):
    "Checks if user has permission for command(commandName)"
    if Server.GetConfig(ctx.message.server.id, "AdminPowerBypass"):
        if ctx.message.channel.permissions_for(ctx.message.author).administrator: return True
    
    hasPerm = False
    for role in ctx.message.author.roles:
        if role.name in Roles.GetRole(ctx.message.server.id):
            if commandName in Roles.GetRole(ctx.message.server.id, role.name,"Permissions"):
                hasPerm = True
    if hasPerm == False:
        print("User does not have permission")
    return hasPerm   