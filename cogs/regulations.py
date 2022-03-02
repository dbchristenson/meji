### Rules Cog ###

### Imports ###

# Library
import nextcord
from nextcord.ext import commands

# Internal
from utils.embeds import embed_regulations


# Cog
class Regulations(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command()
    @commands.has_role('MesiTeam')
    async def regulations(self, ctx: commands.Context):
        '''Prompts Meji to reply with the embed for regulations.'''

        embed = embed_regulations()
        await ctx.send(embed=embed)
        await ctx.message.delete()

def setup(client: commands.Bot):
    client.add_cog(Regulations(client))
