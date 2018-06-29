import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
import os
import shutil
import sys
import configs
import helpers
import logic


def discord_events(bot):
    @bot.event
    async def on_member_join(member):
        #Adding roles in servers StartRoles config.
        await helpers.give_roles(bot, member, configs.get_config(configs.server_config, member.server.id)["JoinRoles"])

        #Announcing user joining to server.
        joinMessage = configs.get_config(configs.server_config, member.server.id)["JoinMessage"].replace("@", member.mention)
        await bot.send_message(member.server.get_channel(configs.get_config(configs.server_config, member.server.id)["MainChannel"]), joinMessage)

    @bot.event
    async def on_ready():
        helpers.check_data_integrity(bot)
        print("Bot Up!")
        for server in bot.servers:
            if configs.get_config(configs.server_config, server.id)["StartMessage"] != "":
                await bot.send_message(server.get_channel(configs.get_config(configs.server_config, server.id)["MainChannel"]), configs.get_config(configs.server_config, server.id)["StartMessage"])
            
            if configs.get_config(configs.bot_config, server.id)["DoSendUpdateMessage"] and configs.get_config(configs.server_config, server.id)["DoGetInfoMessages"]:
                await bot.send_message(server.get_channel(configs.get_config(configs.server_config, server.id)["MainChannel"]), "Info Message:\n```" + configs.get_config(configs.bot_config, server.id)["UpdateMessage"] + "```\nYou can disable this message at anytime with: !config Server DoGetInfoMessages / false")
        helpers.set_bot_config("DoSendUpdateMessage", False)

    @bot.event 
    async def on_server_join(server):
        print(server.id, "has added PhilBot.")
        await bot.send_message(server.get_channel(configs.get_config(configs.server_config, server.id)["MainChannel"]), configs.get_config(configs.server_config, server.id)["StartMessage"])

    @bot.event
    async def on_message(message):
        if not message.author.bot:
          helpers.print_UTF8("Message sent by", message.author, ":", message.content)
          if message.content[0] == "!": 
              args = message.content.split(" ")
              command = args[0].lstrip("!")
              #Removing "!commandname" from args
              args.pop(0)
              if len(args) == 0:
                  target = message.author 
              else: 
                  target = discord.utils.get(message.server.members, name = args[0])

              if command not in configs.get_config(configs.command_config, message.channel.server.id):
                  if helpers.check_permisson(bot, command, message.author):
                      await bot.process_commands(message)
                  else: await bot.send_message(message.channel, configs.get_config(configs.server_config, message.server.id)["NoPermissonMessage"]) 
              else:
                  if helpers.check_permisson(bot, command, message.author):
                      commandDict = configs.get_config(configs.command_config, message.server.id)[command]
                      await logic.execute_function(bot, message.channel, target, commandDict)
                  else: await bot.send_message(message.channel, configs.get_config(configs.server_config, message.server.id)["NoPermissonMessage"]) 

def config(bot):
    @bot.command(pass_context = True)
    async def config(ctx, file = None, *args):
        if file != None:
            returned_value = configs.set_config(ctx.message.channel.server.id, file, args)
            if returned_value != None:
                await bot.say(helpers.format_JSON(file, returned_value))
            else:
                await bot.say("**" + file + " does not exist." + "**")
        else:
            await bot.say("**You must specify a file.**")

    @bot.command(pass_context = True)
    async def reset(ctx, arg = ""):
        print(ctx.message.server.name)
        if arg == ctx.message.server.name:
            shutil.rmtree("Data/" + ctx.message.server.id)
            await bot.say("**Server reset!**")
        else:
            await bot.say("**Please provide your servers exact name.**")

