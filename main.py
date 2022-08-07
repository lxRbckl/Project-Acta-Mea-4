# Project Acta Mea by Alex Arbuckl #


# import <
from os import path
from github import Github
from discord import Intents
from discord.ext import commands
from lxRbckl import githubGet, githubSet, jsonLoad

# >


# global <
gFile = ''
gRepository = ''
gPath = path.realpath(__file__).split('/')
gDirectory = '/'.join(gPath[:(len(gPath) - 1)])
githubToken = ''
actaMea = commands.Bot(command_prefix = '', intents = Intents.all())
discordToken = ''

# >


async def setFunction(ctx, pKeyA: str, pKeyB: str, pElement: str, pData: dict):
    '''  '''

    # if (new node) <
    # elif (then existing node) <
    if ((pKeyA not in pData.keys()) and (not pKeyB) and (not pElement)): var = pData[pKeyA] = {}
    elif (pKeyA in pData.keys()):

        # if (value for key) <
        # elif (then create service) <
        # elif (then add to service) <
        if ((pKeyB != 'service') and (pKeyB)): var = pData[pKeyA][pKeyB] = pElement if (pElement) else []
        elif ((pKeyB not in pData[pKeyA].keys()) and (pKeyB == 'service')): var = pData[pKeyA][pKeyB] = []
        elif ((pKeyB in pData[pKeyA].keys()) and (pElement)): pData[pKeyA][pKeyB].append(pElement); var = 1

        # >

    # >

    # if (data change) <
    if (var is not None): githubSet(

        pData = pData,
        pFile = gFile,
        pRepository = gRepository,
        pGithub = Github(githubToken)

    );

    # >


async def getFunction(ctx, pKeyA: str, pKeyB: str, pElement: str, pData: dict):
    '''  '''

    # if (all nodes) <
    # elif (keys from node) <
    # elif (values from key) <
    if ((not pKeyA) and (not pKeyB)): var = sorted(pData.keys())
    elif ((not pKeyB) and (pKeyA in pData.keys())): var = pData[pKeyA]
    elif (pKeyB in pData[pKeyA].keys()): var = pData[pKeyA][pKeyB] if (pKeyB == 'service') else [pData[pKeyA][pKeyB]]

    # >

    # if (data) <
    if (var): await ctx.channel.send(

        delete_after = 60,
        content = '\n'.join(f'`{i}`' for i in var)

    )

    # >


async def whereFunction(ctx, pKeyA: str, pKeyB: str, pElement: str, pData: dict):
    '''  '''

    # get data <
    # filter data <
    var = {k : [i.lower().split('-') for i in v['service']] for k, v in pData.items()}
    var = [k for k, v in var.items() for i in v if (pKeyA in i)]

    # >

    # if (data) <
    if (len(var) > 0): await ctx.channel.send(

        delete_after = 60,
        content = '\n'.join(f'`{i}`' for i in var)

    )

    # >


async def deleteFunction(ctx, pKeyA: str, pKeyB: str, pElement: str, pData: dict):
    '''  '''

    # if (node) <
    # else (then existing node) <
    if ((pKeyA in pData.keys()) and (not pKeyB) and (not pElement)): del pData[pKeyA]; var = 1
    elif ((pKeyA in pData.keys()) and (pKeyB or pElement)):

        # if (value for node) <
        # elif (service for node services) <
        if (pKeyB != 'service'): del pData[pKeyA][pKeyB]; var = 1
        elif ((pKeyB == 'service') and (pElement)): pData[pKeyA][pKeyB].remove(pElement); var = 1

        # >

    # >

    # if (data change) <
    if (var): githubSet(

        pData = pData,
        pFile = gFile,
        pRepository = gRepository,
        pGithub = Github(githubToken)

    )

    # >


@commands.has_permissions(administrator = True)
@actaMea.command(aliases = jsonLoad(pFile = f'{gDirectory}/setting.json')['aliases'])
async def commandFunction(ctx, pKey: str = None, pValue: str = None, pElement: str = None):
    '''  '''

    await {

        'set' : setFunction,
        'get' : getFunction,
        'del' : deleteFunction,
        'where' : whereFunction,
        'delete' : deleteFunction

    }[ctx.invoked_with.lower()](

        ctx = ctx,
        pKeyA = pKey,
        pKeyB = pValue,
        pElement = pElement,
        pData = githubGet(

            pFile = gFile,
            pRepository = gRepository,
            pGithub = Github(githubToken)

        )

    )


# main <
if (__name__ == '__main__'): actaMea.run(discordToken)

# >
