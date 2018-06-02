import discord
from discord.ext import commands
from discord.ext.commands import Bot
import sys
import json
import os

class Client():
    def __init__(self):
        self.botToken = ""
        try:
            with open("BotConfig.json", 'r') as f:
                self.botToken = json.load(f)["Token"]
            f.close()
        except:
            with open("BotConfig.json", 'w') as f:
                f.write(botConfig)
            f.close()

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