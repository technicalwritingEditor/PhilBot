import client
import discord_events
import asyncio
import datetime
import json
import logic
import discord
import time
import helpers
import configs

client = client.Client()

#Add commands & events here.
discord_events.discord_events(client.bot)
discord_events.config(client.bot)


async def main_bot_loop():
    await client.bot.wait_until_ready()
    await asyncio.sleep(1)
    while True:
        CURRENT_TIME = time.time()
        #Checking each server
        for server in client.bot.servers:
            helpers.check_data_integrity(client.bot)

            #Events
            events = configs.get_config(configs.event_config, server.id)
            events_modified = dict(events)
            for event in events:
                if events[event]["Enabled"]:
                    do_execute = False
                    last_execution = events[event]["LastExecuted"]
                    time_since_last_execution = CURRENT_TIME - last_execution

                    #Execute on TimeOfExecution
                    if events[event]["Repeat"] == "None":
                        event_time = datetime.datetime(events[event]["TimeOfExecution"]["Year"],events[event]["TimeOfExecution"]["Month"],events[event]["TimeOfExecution"]["Day"], events[event]["TimeOfExecution"]["Hour"], events[event]["TimeOfExecution"]["Min"], events[event]["TimeOfExecution"]["Second"])
                        if CURRENT_TIME > event_time.timestamp():
                            do_execute = True
                    
                    #Execute every minute
                    if events[event]["Repeat"] == "Min":
                        if (time_since_last_execution / 60) > 1:
                            do_execute = True
                
                    #Execute every hour
                    if events[event]["Repeat"] == "Hour":
                        if ((time_since_last_execution / 60) / 60) > 1:
                            do_execute = True
                    
                    #Execute every day
                    if events[event]["Repeat"] == "Day":
                        if (((time_since_last_execution / 60) / 60) / 24) > 1:
                            do_execute = True
                 
                    #Execute every week
                    if events[event]["Repeat"] == "Week":
                        if ((((time_since_last_execution / 60) / 60) / 24) / 7) > 1:
                            do_execute = True
                    
                    #Execute every month
                    if events[event]["Repeat"] == "Month":
                        if ((((time_since_last_execution / 60) / 60) / 24) / 30) > 1:
                            do_execute = True

                    if do_execute:
                        print("Executing", event, "in", server.id)
                        
                        await logic.execute_function(client.bot, server.get_channel(configs.get_config(configs.server_config, server.id)["MainChannel"]), events[event], events[event]["Args"])
                       
                        events_modified[event]["LastExecuted"] = CURRENT_TIME
                        
                        #If event is repeating
                        if events[event]["Repeat"] != "Min" and "Hour" and "Day" and "Week" and "Month":
                            del events_modified[event]
                        
            #Writing Changes
            with open("Data/" + server.id + "/EventConfig.json", 'w') as f:
                json.dump(events_modified, f)               

        await asyncio.sleep(1)
        

asyncio.ensure_future(main_bot_loop())

client.RunBot()