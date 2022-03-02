### Handbook Cog ###

### Imports ###

# Library
import nextcord
from nextcord.ext import commands

# Internal
from utils.embeds import embed_handbook


# Cog
class Handbook(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command()
    @commands.has_role('MesiTeam')
    async def handbook(self, ctx: commands.Context, question: str, answer: str, color: str, url: str=None):
        '''Generates an embed to add to the handbook.'''

        embed = embed_handbook(question.strip(), answer.strip(), color.strip().lower(), url)
        await ctx.send(embed=embed)
        await ctx.message.delete()


def setup(client: commands.Bot):
    client.add_cog(Handbook(client))
