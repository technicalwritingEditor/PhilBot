import asyncio
import os
import Config
import json
import shutil

serverConfig = '''{"MainChannel" : "", "JoinRoles" : [],"StartMessage": "","JoinMessage": ""}'''

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
       
        #Deleting server config if it's invalid so it can be recreated.
        try:
            if os.path.exists(serverPath + "/ServerConfig.json"):
                with open(serverPath + "/ServerConfig.json", 'r') as f:
                    config = json.load(f)
                    if config == None:
                        os.remove(serverPath + "/ServerConfig.json")
                f.close()
        except:
            os.remove(serverPath + "/ServerConfig.json")
        
        #Creates new Config if it's missing
        if not os.path.exists(serverPath + "/ServerConfig.json"):
            with open(serverPath + "/ServerConfig.json", 'w') as f:
                f.write(serverConfig)
            f.close()
       
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
            Config.SetConfig(server.id, "MainChannel", selectedChannel.id + "")
            Config.SetConfig(server.id, "JoinMessage", "**Welcome to the server!**")
            Config.SetConfig(server.id, "StartMessage", "**This bot has restarted**")
        
        #Announce bot 
        if sendStartMessage: 
            await bot.send_message(server.get_channel(Config.GetConfig(server.id, "MainChannel")), Config.GetConfig(server.id,"StartMessage"))
    
    #Removing missing servers from Data
    for file in os.listdir("Data"):
        deleteFile = True;
        for server in bot.servers:
            if(server.id == file):
                deleteFile = False
        if deleteFile:
            shutil.rmtree("Data/" + file)
