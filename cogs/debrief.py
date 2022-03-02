### Debrief Cog ###

### Imports ###

# Library
import nextcord
from nextcord.ext import commands

# Internal
from utils.embeds import embed_debrief
from utils.content import DebriefContent


# Cog
class Debrief(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command()
    @commands.has_role('MesiTeam')
    async def debrief_image(self, ctx: commands.Context):
        '''Prompts Meji to send the Mesiverse welcome banner.'''

        content = DebriefContent()

        await ctx.send(content.url)
        await ctx.message.delete()
    
    @commands.command()
    @commands.has_role('MesiTeam')
    async def debrief(self, ctx: commands.Context):
        '''Prompts Meji to send the debrief embed.'''

        embed = embed_debrief()
        await ctx.send(embed=embed)
        await ctx.message.delete()


def setup(client: commands.Bot):
    client.add_cog(Debrief(client))
