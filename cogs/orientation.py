### Orientation Cog ###

### Imports ###

# Library
import nextcord
from nextcord.ext import commands
from tinydb import TinyDB, Query

# Internal
from utils.embeds import embed_orientation
from utils.content import mejibase_path, OrientationContent


# View
class OrientationView(nextcord.ui.View):
    '''A nextcord view for containing the orientation buttons.'''
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.button(label='Welcome, Cadet', style=nextcord.ButtonStyle.blurple, emoji='🙌🏽', custom_id='pv:orientation_button')
    async def orientationbutton(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        '''Initializes the Discord account in the database and grants access to the server.'''

        db = TinyDB(mejibase_path)
        User = Query()

        content = OrientationContent()

        # Check to see if the user is already in the database.
        if db.search(User.user_id == interaction.user.id):
            await interaction.send(content=content.already_registered, ephemeral=True)
        else:
            # Initialize their database entry and upgrade their role.
            db.insert(
                {
                'user_id': interaction.user.id,
                'tokens': 0,
                'affiliation': 'None',
                'wallets': [],
                'collections': [],
                'assets': [],
                'claimable_assets': []
                })
            
            cadet_role = interaction.guild.get_role(938565072379330610)
            member = await interaction.guild.fetch_member(interaction.user.id)
            await member.add_roles(cadet_role)

            await interaction.send(content=content.successfully_registered, ephemeral=True)


# Cog
class Orientation(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.persist = False

    @commands.command()
    @commands.has_role('MesiTeam')
    async def orientation(self, ctx: commands.Context):
        '''Prompts Meji to send the embed and view for orientation functionality.'''

        embed = embed_orientation()
        view = OrientationView()

        await ctx.send(embed=embed, view=view)
        await ctx.message.delete()
    
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.persist:
            self.client.add_view(OrientationView())
            self.persist = True

    

def setup(client: commands.Bot):
    client.add_cog(Orientation(client))
