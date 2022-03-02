### Registrar Cog ###

### Imports ###

# General
import asyncio
import datetime

# Library
import requests
import nextcord
from nextcord.ext import commands

# Internal
from utils.embeds import embed_registrar, embed_wallet, embed_accountinfo, embed_wallet_outcome
from utils.content import FINANCIAL_ADDRESS, RegistrarContent, error_timeout, error_internal, error_explorer, collection_roles, txnbase_path
from utils.user import User
from utils.apis import RequestEndpoints


# Views
class WalletLinkView(nextcord.ui.View):
    '''A nextcord view containing buttons for the wallet link function.'''
    
    def __init__(self, wallet_address: str):
        super().__init__(timeout=None)
        self.value = False
        self.wallet_address = wallet_address
    
    @nextcord.ui.button(label='Confirm', style=nextcord.ButtonStyle.green, emoji='🟩')
    async def confimtxn(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        '''Lets Meji know when to begin checking the central Mesi wallet for a transaction from the address.'''

        # Defer the interaction to give more time for the checking process to occur.
        await interaction.response.defer()

        # Initialize user helper class and check their transactions.
        user = User(interaction.user.id)
        success = await user.checktxns(1, 0, 'Wallet Link', specific_wallet=self.wallet_address)

        self.value = success
        self.clear_items()
        self.stop()

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red, emoji='🟥')
    async def canceltxn(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        '''Cancels the wallet link process by stopping the view.'''

        self.clear_items()
        self.stop()


class RegistrarView(nextcord.ui.View):
    '''A nextcord view containing buttons for performing different registrar functions.'''

    def __init__(self, client: commands.Bot):
        super().__init__(timeout=None)
        self.client = client

    @nextcord.ui.button(label='Link Wallet', style=nextcord.ButtonStyle.blurple, custom_id='pv:link_button')
    async def link_wallet(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        '''Links a wallet address to an account.'''

        # Initalize user helper class.
        user = User(interaction.user.id)

        # Defer the response to allow the user time to give their wallet address.
        await interaction.response.defer()
        
        # Prompt the user to enter their wallet address and wait for a reply
        # from the same channel as the dm.
        embed = embed_wallet()
        wallet_prompt = await interaction.user.send(embed=embed)
        prompt_channel = wallet_prompt.channel

        # Await a wallet address response from the proper dm channel.
        def check(m):
            return m.channel == prompt_channel

        try:
            wallet_response = await self.client.wait_for('message', timeout=30.0, check=check)
            wallet_address = wallet_response.content.strip()
        # Error Handling
        except asyncio.TimeoutError:
            await wallet_prompt.edit(embed=embed_wallet_outcome(False, wallet_prompt.id))
            await interaction.followup.send(content=error_timeout, ephemeral=True)
        except nextcord.errors.Forbidden:   # ignoring inability to remove admin roles
            pass
        except BaseException as e:
            print(e)
            await wallet_prompt.edit(embed=embed_wallet_outcome(False, wallet_prompt.id))
            await interaction.followup.send(content=error_internal, ephemeral=True)
        
        # Define the content obj for responses.
        content = RegistrarContent()

        endpoint = RequestEndpoints().endpoint
        valid_address = requests.get(f'{endpoint}/v2/accounts/{wallet_address}').status_code

        # Check if the address is valid or if the user already linked it.
        if wallet_address in user.wallets or valid_address != 200:
            embed = embed_wallet_outcome(False, interaction.id)
            await wallet_prompt.edit(embed=embed)
            return await interaction.followup.send(content.wallet_used, ephemeral=True)
        else:
            embed.title = content.upd_wallet_title
            embed.description = content.upd_wallet_description + f'`{wallet_address}`'
            embed.add_field(name='Target Wallet', value=f'`{FINANCIAL_ADDRESS}`')
            view = WalletLinkView(wallet_address)
            await wallet_prompt.edit(embed=embed, view=view)
            await view.wait()

        success = view.value

        # Success/Failure
        if success:
            user.add_wallet(wallet_address)
            embed = embed_wallet_outcome(True, wallet_prompt.id, wallet_address)
            await wallet_prompt.edit(embed=embed, view=view)
            await interaction.followup.send(content=content.success_link_reply, ephemeral=True)
        else:
            embed = embed_wallet_outcome(False, wallet_prompt.id)
            await wallet_prompt.edit(embed=embed, view=view)
            await interaction.followup.send(content=content.failure_link_reply, ephemeral=True)

    @nextcord.ui.button(label='Verify Assets', style=nextcord.ButtonStyle.blurple, custom_id='pv:verifyassets_button')
    async def verify_assets(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        '''Checks all of a user's wallet addresses and updates their roles according to which NFTs they hold.'''

        await interaction.response.defer()
        await interaction.send('If you have many assets or many wallets this process may take a while.', ephemeral=True)

        # Initialize user helper class and get the collections the user is holding.
        user = User(interaction.user.id)
        verified_collections = await user.verify_assets()

        if not verified_collections:
            return await interaction.send(content=error_explorer, ephemeral=True)

        roles = []

        # Add the appropriate roles.
        for collection in verified_collections:
            role_id = collection_roles[collection]
            role = interaction.guild.get_role(role_id)
            roles.append(role)
        
        member = await interaction.guild.fetch_member(interaction.user.id)
        await member.add_roles(*roles)

        content = RegistrarContent()
        await interaction.followup.send(content.success_verify_assets, ephemeral=True)

    @nextcord.ui.button(label='Unlink Account', style=nextcord.ButtonStyle.red, custom_id='pv:unlink_button')
    async def unlink_account(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        '''Purges an account from the database and removes their roles.'''

        # Initialize user helper class and delete user from database.
        user = User(interaction.user.id)
        content = RegistrarContent()

        try:
            member = await interaction.guild.fetch_member(user.user_id)
            roles_to_remove = member.roles[1:] # Ignore the @everyone role
            await member.remove_roles(*roles_to_remove, reason='Unlinked Account')

            user.unlink()
        except nextcord.errors.Forbidden:
            await interaction.send(content.permission_failure, ephemeral=True)

        await interaction.send(content.success_unlink, ephemeral=True)

    @nextcord.ui.button(label='Account Info', style=nextcord.ButtonStyle.gray, custom_id='pv:account_info')
    async def account_info(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        '''Sends details to the user about their account.'''

        # Initalize user helper class and get embed.
        user = User(interaction.user.id)
        embed = embed_accountinfo(user, interaction.user.display_name, interaction.user.display_avatar.url)

        await interaction.send(embed=embed, ephemeral=True)


# Cog
class Registrar(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.pv = False
    
    @commands.command()
    @commands.has_role('MesiTeam')
    async def registrar(self, ctx: commands.Context):
        '''Prompts Meji to send the embed and view for the registrar.'''

        embed = embed_registrar()
        view = RegistrarView(self.client)

        await ctx.send(embed=embed, view=view)
    
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.pv:
            self.client.add_view(RegistrarView(self.client))


def setup(client: commands.Bot):
    client.add_cog(Registrar(client))
