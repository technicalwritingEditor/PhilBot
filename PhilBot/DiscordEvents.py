import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
import os
import shutil
import sys
from Config import Server, Roles, CustomCommands
import Helpers
import Logic

def DiscordEvents(bot):
    @bot.event
    async def on_member_join(member):
        #Adding roles in servers StartRoles config.
        await Helpers.GiveRoles(bot, member, Server.GetConfig(member.server.id, "JoinRoles"))

        #Announcing user joining to server.
        joinMessage = Server.GetConfig(member.server.id, "JoinMessage").replace("@", member.mention)
        await bot.send_message(member.server.get_channel(Server.GetConfig(member.server.id, "MainChannel")), joinMessage)

    @bot.event
    async def on_ready():
        Helpers.CheckFileIntegrity(bot)
        print("Bot Up!")
        for server in bot.servers:
            await bot.send_message(server.get_channel(Server.GetConfig(server.id, "MainChannel")), Server.GetConfig(server.id,"StartMessage"))

    @bot.event 
    async def on_server_join(server):
        print(server.id, "has added PhilBot.")
        await bot.send_message(server.get_channel(Server.GetConfig(server.id, "MainChannel")), Server.GetConfig(server.id,"StartMessage"))

    @bot.event
    async def on_message(message):
        if not message.author.bot:
          print("Message sent by", message.author, ":", message.content)
          if message.content[0] == "!": 
              args = message.content.split(" ")
              command = args[0].lstrip("!")
              #Removing "!commandname" from args
              args.pop(0)
              if len(args) == 0:
                  target = message.author 
              else: 
                  target = discord.utils.get(message.server.members, name = args[0])

              if command not in CustomCommands.GetCommands(message.channel.server.id):
                  if Helpers.CheckPermisson(bot, command, message) or command == "powerbypass" and message.channel.permissions_for(message.author).administrator:
                      await bot.process_commands(message)
                  else: await bot.send_message(message.channel, Server.GetConfig(message.server.id, "NoPermissonMessage")) 
              else:
                  if Helpers.CheckPermisson(bot, command, message):
                      commandDict = CustomCommands.GetCommand(message.server.id, command)
                      await Logic.ExecuteFunction(bot, message.channel, target, commandDict)
                  else: await bot.send_message(message.channel, Server.GetConfig(message.server.id, "NoPermissonMessage")) 

def Config(bot):
    @bot.command(pass_context = True)
    async def config(ctx, file = None, *args):
        if file != None:
            returnedValue = Server.Config(ctx.message.channel.server.id, file, args)
            if returnedValue != None:
                await bot.say("**" + file + " config is now : " + str(returnedValue) + "**")
            else:
                await bot.say("**" + file + " does not exist." + "**")
        else:
            await bot.say("**You must specify a file.**")
    
    @bot.command(pass_context = True)
    async def powerbypass(ctx, arg):
        if ctx.message.channel.permissions_for(ctx.message.author).administrator:
            Server.SetConfig(ctx.message.channel.server.id, "AdminPowerBypass", arg)
            await bot.say("**AdminPowerBypass is now : " + str(Server.GetConfig(ctx.message.server.id, "AdminPowerBypass")) + "**")