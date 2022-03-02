### Meji Discord Bot ###

### Imports ###

# General
import traceback
import os

# Library
from nextcord.ext import commands

# Internal
import utils.apis as apis

# Define the client and how to reference it.
client = commands.Bot(command_prefix=commands.when_mentioned)


# Define some utility commands for shutdown and cogs.
@client.command()
@commands.has_role('MesiTeam')
async def shutdown(ctx: commands.Context):
    await ctx.message.delete()
    exit()

@client.command()
async def load(ctx: commands.Context, extension: str):
    client.load_extension(f'cogs.{extension}')
    print(f'{extension} successfully loaded')

@client.command()
async def unload(ctx: commands.Context, extension: str):
    client.unload_extension(f'cogs.{extension}')
    print(f'{extension} successfully unloaded')

@client.command()
async def reload(ctx: commands.Context, extension: str):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print(f'{extension} successfully re-loaded')
    await ctx.message.delete()

# for loop to find cogs folder
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and '_' not in filename:
        try:
            client.load_extension(f'cogs.{filename[:-3]}')
        except BaseException:
            print(traceback.format_exc())
            continue


# Run when ready.
@client.event
async def on_ready():
    print('Mejadi Framework Initialized...')

    apihelper = apis.RequestEndpoints()

    if apihelper.explorer_health != 200:
        print('Failed to connect to AlgoExplorer API')
        if apihelper.purestake_health != 200:
            print('Failed to connect to PureStake API')

client.run(os.environ.get('MEJI_TOKEN'))