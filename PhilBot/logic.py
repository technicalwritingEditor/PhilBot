import helpers
import configs
import discord
import time
import datetime

async def execute_function(bot, channel, object_dict, args):
    async def missing_args():
        await bot.send_message(channel, "**Missing args.**")


    def check_conditionals(bot, dic):
        global target_member
        do_execute = True
        if "containsroles" in dic:
            if not helpers.has_roles(bot, target_member, dic["containsroles"]):
                do_execute = False
        if "haspermisson" in dic:
            for perm in dic["haspermisson"]:
                if not helpers.check_permisson(bot, perm, target_member):
                    do_execute = False
        return do_execute
   
        
    async def execute_attributes(bot, dic):
        global target_member
        global remaining_args
        #Executing layer one attributes

        if "addroles" in dic:
            await helpers.give_roles(bot, target_member, dic["addroles"])

        if "say" in dic:
            message = None
            try:
                message = dic["say"][0]
            except:
                if len(remaining_args) > 0:
                    message = remaining_args[0]
                    del remaining_args[0]

            try:
                send_channel = channel.server.get_channel(dic["say"][1])
            except:
                send_channel = channel
            
            if message != None:
                await bot.send_message(send_channel, message)
            else:
                await missing_args()

        if "removemessages" in dic:
            message = None
            try:
                message = int(dic["removemessages"][0])
            except:
                if len(remaining_args) > 0:
                    message = int(remaining_args[0])
                    del remaining_args[0]

            try:
                send_channel = channel.server.get_channel(dic["removemessages"][1])
            except:
                send_channel = channel
            
            if message != None:
                async for message in bot.logs_from(channel, message):
                    await bot.delete_message(message)
            else:
                await missing_args()

        if "addevent" in dic:
            remaining_args = dic["addevent"] + remaining_args

            event_name = "Event_" + str(len(configs.get_config(configs.event_config, channel.server.id)))
            configs.set_config(channel.server.id, "Events", event_name)
            configs.set_config(channel.server.id, "Events", event_name + " / Functions / " + remaining_args[0])
            del remaining_args[0]
            if remaining_args[0] == "+":
                del remaining_args[0]
                time_of_execution = datetime.datetime.fromtimestamp(time.time() + int(remaining_args[0]))
                del remaining_args[0]
                configs.set_config(channel.server.id, "Events", event_name + " / TimeOfExecution / " + str(time_of_execution.year) + " "  + str(time_of_execution.month) + " "  + str(time_of_execution.day) + " "  + str(time_of_execution.hour) + " "  + str(time_of_execution.minute) + " "  + str(time_of_execution.second))
            else:
                configs.set_config(channel.server.id, "Events", event_name + " / TimeOfExecution / " + remaining_args[0] + " "  + remaining_args[1] + " "  + remaining_args[2] + " "  + remaining_args[3] + " "  + remaining_args[4] + " "  + remaining_args[5])
            remaining_args = remaining_args[6:]
            configs.set_config(channel.server.id, "Events", event_name + " / Args / " + " ".join(remaining_args))
            remaining_args.clear()
            configs.set_config(channel.server.id, "Events", event_name + " / Enabled / true")
 
       
    
    #Getting all attributes or conditionals in object_dict
    attribute_list = []
    for function in object_dict["Functions"]:
        function_dict = configs.get_config(configs.function_config, channel.server.id)[function]
        
        attribute_list += function_dict
        for block in function_dict["if"]:
            attribute_list += function_dict["if"][block]
        for block in function_dict["ifnot"]:
            attribute_list += function_dict["ifnot"][block]
        
    attribute_list = list(set(attribute_list))
    attribute_list.remove("if")
    attribute_list.remove("ifnot")

    #Setting values
    global target_member
    target_member = None

    arg_num = 0
    if "containsroles" in attribute_list or "haspermisson" in attribute_list or "addroles" in attribute_list:
        target_member = discord.utils.get(channel.server.members, id = args[arg_num])
        arg_num += 1
    

    #Args which were not assigned to a specfic var
    global remaining_args
    remaining_args = args[arg_num :]
    print(remaining_args)
    #Execution
    for function in object_dict["Functions"]:
        function_dict = configs.get_config(configs.function_config, channel.server.id)[function]
        #MainBlock       
        await execute_attributes(bot, function_dict)
        
        #Executing conditions blocks
        for block in function_dict["if"]:
            if check_conditionals(bot, function_dict["if"][block]):
                await execute_attributes(bot, function_dict["if"][block])

        for block in function_dict["ifnot"]:
            if not check_conditionals(bot, function_dict["ifnot"][block]):
                await execute_attributes(bot, function_dict["ifnot"][block])

