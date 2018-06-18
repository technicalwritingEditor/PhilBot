import Helpers
from Config import CustomCommands

def CheckConditionals(bot, dic, targetMember):
            doExecute = True
            if "containsroles" in dic:
                if not Helpers.HasRoles(bot, targetMember, dic["containsroles"]):
                    doExecute = False
            if "haspermisson" in dic:
                for perm in dic["haspermisson"]:
                    if not Helpers.CheckPermisson(bot, perm, message):
                        doExecute = False
            return doExecute
        
async def ExecuteAttributes(bot, dic, targetMember, channel):
        #Executing layer one attributes
        if "addroles" in dic:
            await Helpers.GiveRoles(bot, targetMember, dic["addroles"])
        if "say" in dic:
            sayMessage = dic["say"][0]
            if targetMember:
                sayMessage = dic["say"][0].replace("@", targetMember.mention)
            await bot.send_message(channel, sayMessage) 

async def ExecuteFunction(bot, channel, target, functionDict):
    #MainBlock       
    await ExecuteAttributes(bot, functionDict, target, channel)

    #Executing conditions blocks
    for block in functionDict["if"]:
        if CheckConditionals(bot, functionDict["if"][block], target):
            await ExecuteAttributes(bot, functionDict["if"][block], target, channel)

    for block in functionDict["ifnot"]:
        if not CheckConditionals(bot, functionDict["ifnot"][block], target):
            await ExecuteAttributes(bot, functionDict["ifnot"][block], target, channel)

