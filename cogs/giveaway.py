### Giveaway Cog ###

### Imports ###

# Libraries
from nextcord.ext import commands

# Internal
from utils.embeds import embed_giveaway


class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role('MesiTeam')
    async def giveaway(self, ctx: commands.Context):
        '''Prompts Meji to send an interactable '''

        args = ctx.split()

        embed =  embed_giveaway(*args)
    

def setup(client):
    client.add_cog(Giveaway(client))
