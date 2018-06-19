import Helpers
from Config import CustomCommands

def check_conditionals(bot, dic, target_member):
            doExecute = True
            if "containsroles" in dic:
                if not Helpers.has_roles(bot, target_member, dic["containsroles"]):
                    doExecute = False
            if "haspermisson" in dic:
                for perm in dic["haspermisson"]:
                    if not Helpers.check_permisson(bot, perm, message):
                        doExecute = False
            return doExecute
        
async def execute_attributes(bot, dic, target_member, channel):
        #Executing layer one attributes
        if "addroles" in dic:
            await Helpers.give_roles(bot, target_member, dic["addroles"])
        if "say" in dic:
            sayMessage = dic["say"][0]
            if targetMember:
                sayMessage = dic["say"][0].replace("@", targetMember.mention)
            await bot.send_message(channel, sayMessage) 

async def execute_function(bot, channel, target_member, functionDict):
    #MainBlock       
    await execute_attributes(bot, functionDict, target_member, channel)

    #Executing conditions blocks
    for block in functionDict["if"]:
        if check_conditionals(bot, functionDict["if"][block], target_member):
            await execute_attributes(bot, functionDict["if"][block], target_member, channel)

    for block in functionDict["ifnot"]:
        if not check_conditionals(bot, functionDict["ifnot"][block], target_member):
            await execute_attributes(bot, functionDict["ifnot"][block], target_member, channel)

