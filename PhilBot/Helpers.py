import asyncio
import os
from Config import Server
import json
import shutil

serverConfig = '''{"MainChannel" : "", "JoinRoles" : [],"StartMessage": "","JoinMessage": ""}'''
#RolesConfig Format example: {SampleRole : {PermissionLevel : 3, Permissions : ["Perm1", "Perm1"]}}
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