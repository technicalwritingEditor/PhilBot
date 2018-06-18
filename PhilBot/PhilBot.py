import Client
import DiscordEvents
import asyncio
import datetime
import json
import Logic
import discord
import time
from Config import Event, Server

client = Client.Client()

#Add commands & events here.
DiscordEvents.DiscordEvents(client.bot)
DiscordEvents.Config(client.bot)

async def MainBotLoop():
    await client.bot.wait_until_ready()
    await asyncio.sleep(1)
    while True:
        currentTime = time.time()
        #print("------------------\n" + str(currentTime))
        #Checking each server
        for server in client.bot.servers:
            events = Event.GetEvents(server.id)
            eventsModified = dict(events)
            #Checking each event in server
            for event in events:
                if events[event]["Enabled"]:
                    doExecute = False
                    lastExecution = events[event]["LastExecuted"]
                    timeSinceLastExecution = currentTime - lastExecution

                    if events[event]["Repeat"] == "None":
                        eventTime = datetime.datetime(events[event]["TimeOfExecution"]["Year"],events[event]["TimeOfExecution"]["Month"],events[event]["TimeOfExecution"]["Day"], events[event]["TimeOfExecution"]["Hour"], events[event]["TimeOfExecution"]["Min"], events[event]["TimeOfExecution"]["Second"]) 
                        if currentTime > eventTime.timestamp():
                            doExecute = True

                    if events[event]["Repeat"] == "Min":
                        if (timeSinceLastExecution / 60) > 1:
                            doExecute = True
                    
                    if events[event]["Repeat"] == "Hour":
                        if ((timeSinceLastExecution / 60) / 60) > 1:
                            doExecute = True
                    if events[event]["Repeat"] == "Day":
                        if (((timeSinceLastExecution / 60) / 60) / 24) > 1:
                            doExecute = True

                    if events[event]["Repeat"] == "Week":
                        if ((((timeSinceLastExecution / 60) / 60) / 24) / 7) > 1:
                            doExecute = True

                    if events[event]["Repeat"] == "Month":
                        if ((((timeSinceLastExecution / 60) / 60) / 24) / 30) > 1:
                            doExecute = True


                    if doExecute:
                        print("Executing", event, "in", server.id)
                        target = None

                        if events[event]["Target"] != "None":
                            target = discord.utils.get(server.members, name = events[event]["Target"])

                        await Logic.ExecuteFunction(client.bot, server.get_channel(Server.GetConfig(server.id, "MainChannel")), target, events[event])
                       
                        eventsModified[event]["LastExecuted"] = currentTime
                        
                        #If event is repeating
                        if events[event]["Repeat"] != "Min" and "Hour" and "Day" and "Week" and "Month":
                            del eventsModified[event]
                        
            #Writing Changes
            with open("Data/" + server.id + "/EventConfig.json", 'w') as f:
                json.dump(eventsModified, f)               

        #print("------------------\n")
        await asyncio.sleep(1)
        

asyncio.ensure_future(MainBotLoop())

client.RunBot()