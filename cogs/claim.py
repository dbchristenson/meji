### Claim Cog ###

### Imports ###

# Library
import nextcord
from nextcord.ext import commands

# Internal
from utils.embeds import embed_claim, embed_claim_confirm
from utils.user import User


# Views
class ClaimConfirm(nextcord.ui.View):
    '''This view contains the components for sending out the claimable assets.'''

    def __init__(self, claimable_assets: list):
        super().__init__(timeout=300)
        self.claimable_assets = claimable_assets
        self.value = False
    
    @nextcord.ui.Button(label='Confirm Opted In', emoji='🟩', style=nextcord.ButtonStyle.green)
    async def claim_confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        '''Carries out the claim confirmation process.'''

        user_id = interaction.user.id

        self.clear_items()
        self.stop()

class ClaimView(nextcord.ui.View):
    '''This view contains the components for the claim components.'''

    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.Button(label='Claim', emoji='🎁', style=nextcord.ButtonStyle.blurple, custom_id='pv:claim')
    async def claim(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        '''Carries out the claim process for the interacting user.'''

        # Defer the response to give time for the user to complete the interaction.
        await interaction.response.defer()

        # Initialize user helper class.
        user_id = interaction.user.id
        user = User(user_id)

        # Get the assets for the user to claim.
        claimable_assets = user.claimable
        if not claimable_assets:
            return await interaction.followup.send('You do not have any claimable assets.')

        # Send the user the interactable dm.
        embed = embed_claim_confirm(claimable_assets)
        view = ClaimConfirm(claimable_assets)
        await interaction.user.send(embed=embed, view=view)

        await view.wait()
        success = view.value

        if success:
            await interaction.followup.send('Your assets will be sent soon!')
        else:
            await interaction.followup.send('There was an issue with the claim process.')



        


# Cog
class Claim(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.pv = False

    @commands.command()
    @commands.has_role('MesiTeam')
    async def claim(self, ctx: commands.Context):
        '''Prompts Meji to send the claim portal.'''

        embed = embed_claim()
        await ctx.send(embed=embed, view=ClaimView())
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.pv:
            self.client.add_view(ClaimView(self.client))


def setup(client: commands.Bot):
    client.add_cog(Claim(client))
