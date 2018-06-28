import discord
from discord.ext import commands
from discord.ext.commands import Bot
import sys
import json
import os
import Helpers

bot_config = {"Token" : "", "UpdateMessage" : "", "DoSendUpdateMessage" : False}


class Client():
    def __init__(self):
        self.botToken = ""
       
        if not Helpers.check_json("BotConfig.json", bot_config):
            with open("BotConfig.json", 'r') as f:
                config = json.load(f)
            f.close()
            self.botToken = config["Token"]

        if self.botToken == "":
            print("Please set bot token in BotConfig.Json")
            input()
            sys.exit()
        #Creating directories if they don't exist.
        if not os.path.exists("Data"):
            os.mkdir("Data")
        self.bot = commands.Bot(command_prefix = "!")
   
    def RunBot(self):
        self.bot.run(self.botToken)