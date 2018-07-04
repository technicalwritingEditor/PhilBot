import helpers
import configs
import discord
import time
import datetime

async def execute_function(bot, channel, object_dict, args):
    async def missing_args(info = ""):
        await bot.send_message(channel, "**Missing args. " + info + "**")


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
            amount = None
            try:
                amount = dic["say"][0]
            except:
                if len(remaining_args) > 0:
                    amount = remaining_args[0]
                    del remaining_args[0]

            try:
                send_channel = channel.server.get_channel(dic["say"][1])
            except:
                send_channel = channel
            
            if amount != None:
                await bot.send_message(send_channel, amount)
            else:
                await missing_args("No message set for say.")
                return False

        if "removemessages" in dic:
            amount = None
            try:
                amount = int(dic["removemessages"][0])
            except:
                if len(remaining_args) > 0:
                    amount = int(remaining_args[0])
                    del remaining_args[0]

            try:
                send_channel = channel.server.get_channel(dic["removemessages"][1])
            except:
                send_channel = channel
            
            if amount != None:
                async for amount in bot.logs_from(channel, amount):
                    await bot.delete_message(amount)
            else:
                await missing_args("Amount not specified for removemessages")
                return False

        if "addevent" in dic:
            remaining_args = dic["addevent"][1:] + remaining_args
            i = 0
            event_name = "Event_0"
            while str(event_name) in configs.get_config(configs.event_config, channel.server.id):
                event_name = "Event_" + str(i)
                i += 1
            configs.set_config(channel.server.id, "Events", event_name)

            #Functions
            configs.set_config(channel.server.id, "Events", event_name + " / Functions / " + dic["addevent"][0])

            #Execution time
            if remaining_args[0][0] == "+":
                seconds = int(remaining_args[1])
                if len(remaining_args[0]) > 1:
                    if remaining_args[0][1] == "m":
                        seconds = int(remaining_args[1]) * 60
                    if remaining_args[0][1] == "h":
                        seconds = int(remaining_args[1]) * 3600
                    if remaining_args[0][1] == "d":
                        seconds = int(remaining_args[1]) * 86400
                    if remaining_args[0][1] == "w":
                        seconds = int(remaining_args[1]) * 604800
                    if remaining_args[0][1] == "mo":
                        seconds = int(remaining_args[1]) * 2592000
                    if remaining_args[0][1] == "y":
                        seconds = int(remaining_args[1]) * 31536000
                del remaining_args[0]
                del remaining_args[0]
                time_of_execution = datetime.datetime.fromtimestamp(time.time() + seconds)
                configs.set_config(channel.server.id, "Events", event_name + " / TimeOfExecution / " + str(time_of_execution.year) + " "  + str(time_of_execution.month) + " "  + str(time_of_execution.day) + " "  + str(time_of_execution.hour) + " "  + str(time_of_execution.minute) + " "  + str(time_of_execution.second))
            else:
                if len(remaining_args) < 6:
                    configs.set_config(channel.server.id, "Events", event_name + " / TimeOfExecution / " + remaining_args[0] + " "  + remaining_args[1] + " "  + remaining_args[2] + " "  + remaining_args[3] + " "  + remaining_args[4] + " "  + remaining_args[5])
                    remaining_args = remaining_args[6:]
                else:
                    await missing_args("No time set for addevent.")
                    return False

        
            #Args
            #Checks if addevent needs target_member if so adds it to it's args.
            attributes_in_event = get_required_attributes(dic["addevent"][0])
            if "containsroles" in attributes_in_event or "haspermisson" in attributes_in_event or "addroles" in attributes_in_event:
                remaining_args = [target_member.id] + remaining_args
            configs.set_config(channel.server.id, "Events", event_name + " / Args / " + " ".join(remaining_args))
            remaining_args.clear()

            configs.set_config(channel.server.id, "Events", event_name + " / Enabled / true")


    def get_required_attributes(functions):
        attribute_list = []
        if type(functions) == str:
            functions = [functions]

        for function in functions:
            function_dict = configs.get_config(configs.function_config, channel.server.id)[function]

            #Main
            for object in function_dict:
                attribute_list += [object]
                if object == "addevent":
                    attribute_list += get_required_attributes(function_dict[object][0])

            #if
            for block in function_dict["if"]:
                for object in function_dict["if"][block]:
                    attribute_list += [object]
                    if object == "addevent":
                        attribute_list += get_required_attributes(function_dict["if"][block][object][0])

            #ifnot
            for block in function_dict["ifnot"]:
                for object in function_dict["ifnot"][block]:
                    attribute_list += [object]
                    if object == "addevent":
                        attribute_list += get_required_attributes(function_dict["ifnot"][block][object][0])

        #Removing unnecessary objects 
        attribute_list = list(set(attribute_list))
        if "if" in attribute_list: attribute_list.remove("if")
        if "ifnot" in attribute_list: attribute_list.remove("ifnot")
        return attribute_list

    attribute_list = get_required_attributes(object_dict["Functions"])

    #Setting values
    global target_member
    target_member = None
    
    arg_num = 0
    if "containsroles" in attribute_list or "haspermisson" in attribute_list or "addroles" in attribute_list:
        if len(args) > 0:
            target_member = discord.utils.get(channel.server.members, id = args[arg_num])
            arg_num += 1
        else:
            await missing_args("No target user set.")
            return False
    

    #Args which were not assigned to a specfic var
    global remaining_args
    remaining_args = args[arg_num :]
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
    return True

