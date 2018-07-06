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

bot_client = client.Client()
bot_client.bot.remove_command('help')
#Add commands & events here.
discord_events.discord_events(bot_client.bot)
discord_events.config(bot_client.bot)


async def main_bot_loop():
    await bot_client.bot.wait_until_ready()
    await asyncio.sleep(1)
    while True:
        CURRENT_TIME = time.time()
        #Checking each server
        for server in bot_client.bot.servers:
            helpers.check_data_integrity(bot_client.bot)

            #Events
            events = configs.get_config(configs.event_config, server.id)
            events_to_delete = []
            for event in events:
                if events[event]["Enabled"]:
                    do_execute = False
                    last_execution = events[event]["LastExecuted"]
                    time_since_last_execution = CURRENT_TIME - last_execution

                    #Execute on TimeOfExecution
                    if events[event]["Repeat"] == "None":
                        try:
                            event_time = datetime.datetime(events[event]["TimeOfExecution"]["Year"],events[event]["TimeOfExecution"]["Month"],events[event]["TimeOfExecution"]["Day"], events[event]["TimeOfExecution"]["Hour"], events[event]["TimeOfExecution"]["Min"], events[event]["TimeOfExecution"]["Second"])
                            if CURRENT_TIME > event_time.timestamp():
                                do_execute = True
                        except:
                            await bot_client.bot.send_message(server.get_channel(configs.get_config(configs.server_config, server.id)["MainChannel"]), "**Invalid time set in event " + event + ". Disabling.**")
                            configs.set_config(server.id, "Events", event + " / Enabled / false")
                        
                    
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
                        await logic.execute_function(bot_client.bot, server.get_channel(configs.get_config(configs.server_config, server.id)["MainChannel"]), events[event], events[event]["Args"])
                        configs.set_config(server.id, "Events", event + " / LastExecuted / " + str(int(CURRENT_TIME)))
                        #If event is not repeating
                        if events[event]["Repeat"] != "Min" and "Hour" and "Day" and "Week" and "Month":
                            events_to_delete.append(event)
            #Writing Changes
            configs.set_config(server.id, "Events", events_to_delete)         
        await asyncio.sleep(1)
        

asyncio.ensure_future(main_bot_loop())

bot_client.RunBot()