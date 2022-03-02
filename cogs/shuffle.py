### Shuffle Cog ###

### Imports ###

# General
import json

# Library
import nextcord
from nextcord.ext import commands
from tinydb import TinyDB, Query
from utils import embeds

# Internal
from utils.content import ShuffleContent
from utils.embeds import embed_shuffle, embed_invalid_shuffle, embed_shuffle_records, embed_payment, embed_unsuccesful_pay, embed_successful_pay
from utils.shufflehelper import ShuffleHelper
from utils.user import User


# Initialize database.
shuffles_path = 'databases/shuffles.json'
db = TinyDB(shuffles_path)
Shuffle = Query()


# Views
class ShuffleView(nextcord.ui.View):
    '''Stores the components for a valid shuffle element.'''
    def __init__(self, client):
        super().__init__(timeout=None)
        self.client = client
        self.active = True

    @nextcord.ui.button(label='Enter', emoji='🎲', style=nextcord.ButtonStyle.blurple, custom_id='pv:enter_shuffle')
    async def enter_shuffle(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        '''Enters the user into the shuffle linked to the embed element.'''

        # Defer the interaction to give time to complete the transaction.
        await interaction.response.defer()

        # Initialize the shuffle helper class.
        element_id = interaction.message.id
        Shuffle = ShuffleHelper(element_id)

        # Setup the embed and view for the payment message.
        pay_embed = embed_payment(Shuffle.price)
        pay_view = PaymentView(Shuffle.price)
        await interaction.user.send(embed=pay_embed, view=pay_view)

        await pay_view.wait()
        success = pay_view.value

        content = ShuffleContent(Shuffle.collection, Shuffle.available, Shuffle.price, Shuffle.shuffle_type)

        if success:
            # This block of text updates the databases.
            await interaction.followup.send(content.successful_entry, ephemeral=True)

            # Initialize user helper class.
            user_id = interaction.user.id

            # Get the first 'unassigned' asset.
            assigned_asset = [(asset, idx) for idx, asset in enumerate(Shuffle.assets) if asset['assigned'] == False][0]
            asset, idx = assigned_asset

            # Update the asset to mark it as assigned.
            asset['assigned'] = True
            updated_assets = Shuffle.assets[idx] = asset

            # Update the entries.
            updated_entry = Shuffle.entries.append(
                {
                'user_id': user_id, 
                'assigned_asset': asset, 
                'sent': False,
                'shuffle_id': interaction.message.id
                })

            remaining = Shuffle.decrement_shuffle()

            Shuffle.db.update(
                {
                'assets': updated_assets,          # updates the assigned asset so it won't be reused
                'entries': updated_entry,          # appends the new entry to the existing ones
                'remaining': remaining             # int representing remaining assets
                }, Shuffle.Shuffle.id == Shuffle.id)

            # Updates user database for claim portal.
            user_help = User(user_id)
            upd_claimable = user_help.claimable.append(asset)
            user_help.db.upsert({'claimable': upd_claimable}, user_help.Query.id == user_id)

            # Shutdown shuffle is all assets are exhausted.
            if remaining == 0:
                self.active = False
                await self.shutdown(interaction.message.id)
        else:
            await interaction.followup.send(content.unsuccessful_entry, ephemeral=True)
    
    @nextcord.ui.button(label='Records', emoji='🎟', style=nextcord.ButtonStyle.grey, custom_id='pv:shuffle_records')
    async def user_records(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        '''Responds with data about how the user has interacted with the shuffle previously.'''

        # Obtain relevant data needed for displaying records.
        user_id = interaction.user.id
        display_name = interaction.user.display_name
        display_avatar = interaction.user.display_avatar
        element_id = interaction.message.id
        shuffle = ShuffleHelper(element_id)

        user_entries = shuffle.get_entries(user_id)

        embed = embed_shuffle_records(display_name, display_avatar, element_id, user_entries)

        await interaction.send(embed=embed, ephemeral=True)
    
    async def shutdown(self, message_id: int):
        '''A method for shutting down the shuffle.'''

        msg = await self.client.fetch_message(message_id)
        embed = embed_invalid_shuffle()
        await msg.edit(embed=embed, view=RecordsOnlyView())


class PaymentView(nextcord.ui.View):
    '''A view containing the components for entry payment.'''

    def __init__(self, price: int):
        super().__init__()
        self.value = False
        self.price = int(price)
    
    @nextcord.ui.button(label='Confirm', style=nextcord.ButtonStyle.green, emoji='🟩')
    async def confirmtxn(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        '''Lets Meji know when to begin searching for the transaction.'''

        # Defer the interaction again to give Meji time to search for the txn.
        await interaction.response.defer()

        # Initialize the user helper class and check their transactions.
        user = User(interaction.user.id)
        success = await user.checktxns(1, self.price, 'Shuffle Entry', checks=1)
        
        if success:
            embed = embed_successful_pay(interaction.id)
            self.value = success
            await interaction.message.edit(embed=embed, view=None)
            self.stop()
        else:
            self.value = success
            embed = embed_unsuccesful_pay(interaction.id)
            await interaction.message.edit(embed=embed, view=None)
            self.stop()
        
        await interaction.followup.send('Thanks for choosing the Mesiverse!', ephemeral=True)
    
    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red, emoji='🟥')
    async def canceltxn(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        '''Cancels the checking process for the shuffle entry.'''

        embed = embed_unsuccesful_pay(interaction.id)
        await interaction.edit(embed=embed, view=None)


class RecordsOnlyView(nextcord.ui.View):
    '''A view only with the records button for invalid shuffles.'''

    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label='Records', emoji='🎟', style=nextcord.ButtonStyle.grey, custom_id='pv:shuffle_only_records')
    async def user_records(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        '''Responds with data about how the user has interacted with the shuffle previously.'''

        # Obtain relevant data needed for displaying records.
        user_id = interaction.user.id
        display_name = interaction.user.display_name
        display_avatar = interaction.user.display_avatar
        element_id = interaction.message.id
        shuffle = ShuffleHelper(element_id)

        user_entries = shuffle.get_entries(user_id)

        embed = embed_shuffle_records(display_name, display_avatar, element_id, user_entries)

        await interaction.send(embed=embed, ephemeral=True)


# Cog
class Shuffle(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.pv = False
    
    # Generates shuffle command.
    @commands.command()
    @commands.has_role('MesiTeam')
    async def shuffle(self, ctx: commands.Context, collection: str, available: str, price: str, shuffle_type: str, url: str = None):
        '''Generates shuffle module that can be entered into.'''

        # Transform some parameters.
        available = int(available)
        price = int(price)

        # Testing mode enabled y/n
        if url == 'test':
            embed = embed_shuffle(collection, available, price, shuffle_type, None)
            view = ShuffleView(self.client)

            await ctx.send('@everyone', embed=embed, view=view)
            await ctx.message.delete()
        else:
            embed = embed_shuffle(collection, available, price, shuffle_type, url)
            view = ShuffleView(self.client)

            shuffle_element = await ctx.send('@everyone', embed=embed, view=view)

            # Initialize the database entry for the shuffle.
            db.insert({
                'id': shuffle_element.id,
                'collection': collection, 
                'available': available,
                'remaining': available,
                'price': price,
                'shuffle_type': shuffle_type,
                'assets': [],
                'entries': []
                })
            
            # Add assets from the collection to the shuffle element.
            shuffle = ShuffleHelper(shuffle_element.id)
            shuffle.add_assets()
        
        await ctx.message.delete()

    # Format static data for collections.
    @commands.command()
    @commands.has_role('MesiTeam')
    async def convert_static(self, ctx: commands.Context):
        '''Converts static json files of creator wallet assets and formats them into useable data.'''

        collection = ctx.message.content.split()[2].strip().lower()

        # Initialize local database.
        static_db_path = f'databases/{collection}.json'
        open(static_db_path, 'w+')
        static_db = TinyDB(static_db_path)

        # Load in the static data and map important values.
        assets = json.load(open(f'static/{collection}.json'))['assets']

        for asset in assets:
            asset_idx = asset['index']
            asset_name = asset['params']['name']
            asset_unit = asset['params']['unit-name']
            asset_code = ''.join(filter(str.isdigit, asset_unit))

            static_db.insert({
                'asset_id': asset_idx,
                'asset_name': asset_name,
                'asset_unit': asset_unit,
                'asset_code': asset_code,
                'used_in_shuffle': False,
                'owned': True
                })
        
        await ctx.send(f'Static data for `{collection}` formatted successfully.')
        await ctx.message.delete()

    # Command to prompt Meji to mark a shuffle as invalid. 
    @commands.command()
    @commands.has_role('MesiTeam')
    async def shuffle_invalidate(self, ctx: commands.Context):
        '''Prompts Meji to change a shuffle to invalid which denies further entries to it.'''

        element_id = int(ctx.message.content.split()[2].strip().lower())
        element = await ctx.channel.fetch_message(element_id)
        Shuffle = ShuffleHelper(element_id)

        embed = embed_invalid_shuffle(Shuffle.collection, Shuffle.available, Shuffle.price, Shuffle.shuffle_type)
        view = RecordsOnlyView()

        await element.edit(embed=embed, view=view)
        await ctx.message.delete()
    
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.pv:
            self.client.add_view(ShuffleView(self.client))
            self.client.add_view(RecordsOnlyView())


def setup(client):
    client.add_cog(Shuffle(client))
