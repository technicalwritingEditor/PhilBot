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

def Events(bot):
    @bot.event
    async def on_member_join(member):
        #Adding roles in servers StartRoles config.
        await Helpers.GiveRoles(bot, member, Server.GetConfig(member.server.id, "JoinRoles"))

        #Announcing user joining to server.
        joinMessage = Server.GetConfig(member.server.id, "JoinMessage").replace("@", member.mention)
        await bot.send_message(member.server.get_channel(Server.GetConfig(member.server.id, "MainChannel")), joinMessage)

    @bot.event
    async def on_ready():
        await Helpers.CheckFileIntegrity(bot) 
        print("Bot Up!")
        for server in bot.servers:
            await bot.send_message(server.get_channel(Server.GetConfig(server.id, "MainChannel")), Server.GetConfig(server.id,"StartMessage"))

    @bot.event 
    async def on_server_join(server):
        print(server.id, "has added PhilBot.")
        await Helpers.CheckFileIntegrity(bot) 
        await bot.send_message(server.get_channel(Server.GetConfig(server.id, "MainChannel")), Server.GetConfig(server.id,"StartMessage"))

    @bot.event
    async def on_message(message):
        def CheckConditionals(dic, targetMember):
            doExecute = True
            if "containsroles" in dic:
                if not Helpers.HasRoles(bot, targetMember, dic["containsroles"]):
                    doExecute = False
            if "haspermisson" in dic:
                for perm in dic["haspermisson"]:
                    if not Helpers.CheckPermisson(bot, perm, message):
                        doExecute = False
            return doExecute
        
        async def ExecuteAttributes(bot, dic, targetMember):
             #Executing layer one attributes
             if "addroles" in dic:
                 await Helpers.GiveRoles(bot, target, dic["addroles"])
             if "say" in dic:
                 sayMessage = dic["say"][0].replace("@", targetMember.mention)
                 await bot.send_message(message.channel, sayMessage) 

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
                      #Custom command code
                      commandDic = CustomCommands.GetCommand(message.server.id, command)
                      
                      await ExecuteAttributes(bot, commandDic, target)

                      #Executing conditions
                      for block in commandDic["if"]:
                          if CheckConditionals(commandDic["if"][block], target):
                              await ExecuteAttributes(bot, commandDic["if"][block], target)

                      for block in commandDic["ifnot"]:
                          if not CheckConditionals(commandDic["ifnot"][block], target):
                              await ExecuteAttributes(bot, commandDic["ifnot"][block], target)
                  else: await bot.send_message(message.channel, Server.GetConfig(message.server.id, "NoPermissonMessage")) 

def Config(bot):
    @bot.command(pass_context = True)
    async def powerbypass(ctx, arg):
        if ctx.message.channel.permissions_for(ctx.message.author).administrator:
            Server.SetConfig(ctx.message.channel.server.id, "AdminPowerBypass", arg)
            await bot.say("AdminPowerBypass is now : " + str(Server.GetConfig(ctx.message.server.id, "AdminPowerBypass")))
    
    @bot.command(pass_context = True)
    async def config(ctx, key = "", *args):
        if key != "":
            if len(args) > 0:
                Server.SetConfig(ctx.message.channel.server.id, key, args)
            await bot.say(key + " is currently : " + str(Server.GetConfig(ctx.message.server.id, key)))
        else:
            await bot.say("Server config : " + str(Server.GetConfig(ctx.message.server.id)))
   
    #Roles
    @bot.command(pass_context = True)
    async def role(ctx, *args):
        if len(args) > 0:
            Roles.SetRole(ctx.message.channel.server.id, args)
        await bot.say("RolesConfig currently contains : " + str(Roles.GetRole(ctx.message.channel.server.id)))
    
    @bot.command(pass_context = True)
    async def perm(ctx, key, *args):
        Roles.SetPermissons(ctx.message.channel.server.id, key, args)
        await bot.say("RolesConfig currently contains : " + str(Roles.GetRole(ctx.message.channel.server.id)))

def Commands(bot): 
    @bot.command(pass_context = True)
    async def ping(ctx):
        await bot.say("Pong!")

    @bot.command(pass_context = True)
    async def say(ctx, *args):
        await bot.say(Helpers.ToString(args))
   
    #Custom commands
    @bot.command(pass_context = True)
    async def command(ctx, *args):
        CustomCommands.SetCommand(ctx.message.channel.server.id, args)
   
    @bot.command(pass_context = True)
    async def block(ctx, command, type, *args):
        CustomCommands.SetBlock(ctx.message.channel.server.id, command, type, args)
    
    @bot.command(pass_context = True)
    async def attribute(ctx, command, *args):
        CustomCommands.SetAttribute(ctx.message.channel.server.id, command, args)
   
    @bot.command(pass_context = True)
    async def attributevalue(ctx, command, attribute, *args):
        CustomCommands.SetAttributeValue(ctx.message.channel.server.id, command, attribute, args)
    
    @bot.command(pass_context = True)
    async def blockattribute(ctx, command, type, block, *args):
        CustomCommands.SetBlockAttribute(ctx.message.channel.server.id, command, type, block, args)

    @bot.command(pass_context = True)
    async def blockattributevalue(ctx, command, type, block, condition, *args):
        CustomCommands.SetBlockAttributeValue(ctx.message.channel.server.id, command, type, block, condition, args)