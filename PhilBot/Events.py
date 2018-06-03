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
        await bot.send_message(member.server.get_channel(Server.GetConfig(member.server.id, "MainChannel")), joinMessage)

    @bot.event
    async def on_ready():
        await Helpers.UpdateData(bot, True)
        print("Bot Up!")

    @bot.event 
    async def on_server_join(server):
        print(server.id, "has added PhilBot.")
        await Helpers.UpdateData(bot) 

def Commands(bot):
    #Config
    #Server
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

    #General   
    @bot.command(pass_context = True)
    async def ping(ctx):
        await bot.say("Pong!")

    @bot.command(pass_context = True)
    async def say(ctx, *args):
        #Converting args to a string.
        await bot.say(Helpers.ToString(args))


