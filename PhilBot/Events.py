import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
import os
import shutil
import sys
from Config import Server, Roles
import Helpers

def Events(bot):
    @bot.event
    async def on_member_join(member):
        #Adding roles in servers StartRoles config.
        rolesStr = Server.GetConfig(member.server.id, "JoinRoles")
        roles = []
        for role in rolesStr:
            roles.append(discord.utils.get(member.server.roles, name = role))
        await bot.add_roles(member, *roles)
        print("User", member.name, "Joined", member.server.id, "adding roles", rolesStr) 

        joinMessage = Server.GetConfig(member.server.id, "JoinMessage")
        #Adding user mentions.
        splitJoinMessage = joinMessage.split()
        i = 0
        indexs = []
        for char in splitJoinMessage:
            if char == "@":
                splitJoinMessage.pop(i)
                splitJoinMessage.insert(i, member.mention)
            i += 1
        joinMessage = " ".join(splitJoinMessage)

        #Announcing user joining to server.
        await bot.say(member.server.get_channel(Server.GetConfig(member.server.id, "MainChannel")), joinMessage)

    @bot.event
    async def on_ready():
        await Helpers.UpdateData(bot)
        print("Bot Up!")

    @bot.event 
    async def on_server_join(server):
        print(server.id, "has added PhilBot.")
        await Helpers.UpdateData(bot) 
        await bot.send_message(server.get_channel(Server.GetConfig(server.id, "MainChannel")), Server.GetConfig(server.id,"StartMessage"))

def Config(bot):
    @bot.command(pass_context = True)
    async def powerbypass(ctx, arg):
        if ctx.message.channel.permissions_for(ctx.message.author).administrator:
            Server.SetConfig(ctx.message.channel.server.id, "AdminPowerBypass", arg)
            await bot.say("AdminPowerBypass is now : " + str(Server.GetConfig(ctx.message.server.id, "AdminPowerBypass")))
    
    @bot.command(pass_context = True)
    async def config(ctx, key = "", *args):
        if await Helpers.CheckPermisson(bot, "config", ctx):
            if key != "":
                if len(args) > 0:
                    Server.SetConfig(ctx.message.channel.server.id, key, args)
                await bot.say(key + " is currently : " + str(Server.GetConfig(ctx.message.server.id, key)))
            else:
                await bot.say("Server config : " + str(Server.GetConfig(ctx.message.server.id)))
   
    #Roles
    @bot.command(pass_context = True)
    async def role(ctx, *args):
        if await Helpers.CheckPermisson(bot, "role", ctx):
            if len(args) > 0:
                Roles.SetRole(ctx.message.channel.server.id, args)
            await bot.say("RolesConfig currently contains : " + str(Roles.GetRole(ctx.message.channel.server.id)))
    
    @bot.command(pass_context = True)
    async def perm(ctx, key, *args):
        if await Helpers.CheckPermisson(bot, "perm", ctx): 
            Roles.SetPermissons(ctx.message.channel.server.id, key, args)
            await bot.say("RolesConfig currently contains : " + str(Roles.GetRole(ctx.message.channel.server.id)))

def Commands(bot): 
    @bot.command(pass_context = True)
    async def ping(ctx):
        if await Helpers.CheckPermisson(bot, "ping", ctx):     
            await bot.say("Pong!")

    @bot.command(pass_context = True)
    async def say(ctx, *args):
        if await Helpers.CheckPermisson(bot, "say", ctx): 
            await bot.say(Helpers.ToString(args))


