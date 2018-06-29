import helpers
import configs

def check_conditionals(bot, dic, target_member, server):
            do_execute = True
            if "containsroles" in dic:
                if not helpers.has_roles(bot, target_member, dic["containsroles"]):
                    do_execute = False
            if "haspermisson" in dic:
                for perm in dic["haspermisson"]:
                    if not helpers.check_permisson(bot, perm, target_member):
                        do_execute = False
            return do_execute
   
        
async def execute_attributes(bot, dic, target_member, channel):
        #Executing layer one attributes
        if "addroles" in dic:
            await helpers.give_roles(bot, target_member, dic["addroles"])
        if "say" in dic:
            say_message = dic["say"][0]
            if target_member:
                say_message = dic["say"][0].replace("@", target_member.mention)
            await bot.send_message(channel, say_message) 


async def execute_function(bot, channel, target_member, objectDict):
   
    for function in objectDict["Functions"]:
        function_dict = configs.get_config(configs.function_config, channel.server.id)[function]
        #MainBlock       
        await execute_attributes(bot, function_dict, target_member, channel)
        
        #Executing conditions blocks
        for block in function_dict["if"]:
            if check_conditionals(bot, function_dict["if"][block], target_member, channel.server):
                await execute_attributes(bot, function_dict["if"][block], target_member, channel)

        for block in function_dict["ifnot"]:
            if not check_conditionals(bot, function_dict["ifnot"][block], target_member, channel.server):
                await execute_attributes(bot, function_dict["ifnot"][block], target_member, channel)