### Connections Cog ###

### Imports ###

# Library
import nextcord
from nextcord.ext import commands

# Internal
from utils.content import ConnectionsContent
from utils.embeds import embed_connections


# View
class ConnectionsView(nextcord.ui.View):
    '''A nextcord view containing buttons for the connections channel.'''
    def __init__(self):
        super().__init__(timeout=None)
        
        content = ConnectionsContent()
        
        self.add_item(nextcord.ui.Button(label=content.link1['label'], url=content.link1['url'], emoji=content.link1['emoji']))     # website
        self.add_item(nextcord.ui.Button(label=content.link2['label'], url=content.link2['url'], emoji=content.link2['emoji']))     # nft explorer
        self.add_item(nextcord.ui.Button(label=content.link3['label'], url=content.link3['url'], emoji=content.link3['emoji']))     # twitter
        self.add_item(nextcord.ui.Button(label=content.link4['label'], url=content.link4['url'], emoji=content.link4['emoji']))     # git


# Cog
class Connections(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command()
    @commands.has_role('MesiTeam')
    async def connections(self, ctx: commands.Context):
        '''Generates an embed for the connections channel.'''

        embed = embed_connections()
        view = ConnectionsView()

        await ctx.send(embed=embed, view=view)
        await ctx.message.delete()


def setup(client: commands.Bot):
    client.add_cog(Connections(client))
