import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
import os
import shutil
import sys
import Config 
import Helpers

def Events(bot):
    @bot.event
    async def on_member_join(member):
        #Adding roles in servers StartRoles config.
        rolesStr = Config.GetConfig(member.server.id, "JoinRoles")
        roles = []
        for role in rolesStr:
            roles.append(discord.utils.get(member.server.roles, name = role))
        await bot.add_roles(member, *roles)
        print("User", member.name, "Joined", member.server.id, "adding roles", rolesStr) 

        joinMessage = Config.GetConfig(member.server.id, "JoinMessage")
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
        await bot.send_message(member.server.get_channel(Config.GetConfig(member.server.id, "MainChannel")), joinMessage)

    @bot.event
    async def on_ready():
        await Helpers.UpdateData(bot, True)
        print("Bot Up!")

    @bot.event 
    async def on_server_join(server):
        print(server.id, "has added PhilBot.")
        await Helpers.UpdateData(bot) 

def Commands(bot):
    @bot.command(pass_context = True)
    async def getconfig(ctx, key):
            await bot.say("Key of " + key + " is currently " + str(Config.GetConfig(ctx.message.server.id, key)))

    @bot.command(pass_context = True)
    async def config(ctx, key, *args):
            Config.SetConfig(ctx.message.channel.server.id, key, args)
            await bot.say("Key of " + key + " is now " + str(Config.GetConfig(ctx.message.server.id, key)))

    @bot.command(pass_context = True)
    async def ping(ctx):
        await bot.say("Pong!")

    @bot.command(pass_context = True)
    async def say(ctx, *args):
        #Converting args to a string.
        await bot.say(Helpers.ToString(args))


