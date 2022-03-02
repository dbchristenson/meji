# Imports #

# Library
import nextcord

# Internal
from utils.content import (RegulationContent, ConnectionsContent, DebriefContent, 
                           OrientationContent, RegistrarContent, UserInfoContent, 
                           ShuffleContent, ShuffleUserRecordsContent, ShufflePaymentContent,
                           ClaimContent, FINANCIAL_ADDRESS)


# Debrief Embeds #
def embed_debrief():
    '''Generates the embed for the debrief channel.'''

    content = DebriefContent()

    embed = nextcord.Embed()
    embed.title = content.title
    embed.description = content.description
    embed.color = nextcord.Color.purple()

    embed.add_field(name=content.field1['name'], value=content.field1['value'], inline=False)
    embed.add_field(name=content.field2['name'], value=content.field2['value'], inline=False)
    embed.add_field(name=content.field3['name'], value=content.field3['value'], inline=False)
    embed.add_field(name=content.field4['name'], value=content.field4['value'], inline=False)

    embed.set_footer(text=content.footer)

    return embed

# Regulations Embeds #
def embed_regulations():
    '''Generates the embed for the regulations channel.'''
    
    content = RegulationContent()

    embed = nextcord.Embed()
    embed.title = content.title
    embed.description = content.description
    embed.color = nextcord.Color.purple()

    embed.add_field(name=content.field1['name'], value=content.field1['value'], inline=False)
    embed.add_field(name=content.field2['name'], value=content.field2['value'], inline=False)
    embed.add_field(name=content.field3['name'], value=content.field3['value'], inline=False)
    embed.add_field(name=content.field4['name'], value=content.field4['value'], inline=False)

    return embed


# Handbook Embeds #
def embed_handbook(question: str, answer: str, embed_color: str, url):
    '''Generates the embeds for the handbook channel.'''

    embed = nextcord.Embed()
    embed.title = f'Q: {question}'
    embed.description = f'> **A:** {answer}'
    embed.color = getattr(nextcord.Color, embed_color)()

    if url:
        embed.set_image(url=url)

    return embed


# Connections Embeds #
def embed_connections():
    '''Generates the embed for the connections channel.'''

    content = ConnectionsContent()

    embed = nextcord.Embed()
    embed.title = content.title
    embed.description = content.description
    embed.color = nextcord.Color.purple()

    embed.set_footer(text=content.footer)
    embed.set_thumbnail(url=content.url)

    return embed


# Orientation Embeds #
def embed_orientation():
    '''Generates the embed for the orientation channel.'''

    content = OrientationContent()

    embed = nextcord.Embed()
    embed.title = content.title
    embed.description = content.description
    embed.color = nextcord.Color.purple()

    embed.set_thumbnail(url=content.thumbnail_url)

    return embed


# Registrar Embeds #
def embed_registrar():
    '''Generates the embed for the registrar channel.'''

    content = RegistrarContent()

    embed = nextcord.Embed()
    embed.title = content.title
    embed.description = content.description
    embed.color = nextcord.Color.purple()

    embed.add_field(name=content.field1['name'], value=content.field1['value'], inline=False)
    embed.add_field(name=content.field2['name'], value=content.field2['value'], inline=False)
    embed.add_field(name=content.field3['name'], value=content.field3['value'], inline=False)
    embed.add_field(name=content.field4['name'], value=content.field4['value'], inline=False)
    embed.set_footer(text=content.footer)

    return embed

def embed_wallet():
    '''Generates embed for the wallet request function.'''

    content = RegistrarContent()

    embed = nextcord.Embed()
    embed.title = content.wallet_title
    embed.description = content.wallet_description
    embed.color = nextcord.Color.purple()

    embed.set_footer(text=content.wallet_footer)

    return embed

def embed_wallet_outcome(outcome: bool, id: int, address=None):
    '''Generates embed for the outcome of the wallet request function.'''

    content = RegistrarContent()
    embed = nextcord.Embed()
    embed.title = content.completed_wallet_title + f'`{id}`'

    if outcome:
        embed.description = content.success_link
        embed.color = nextcord.Color.green()

        embed.add_field(name='Selected Wallet Address', value=f'`{address}`', inline=False)
    else:
        embed.description = content.failure_link
        embed.color = nextcord.Color.red()

        embed.set_footer(text=content.failure_link_reasons)

    return embed

def embed_accountinfo(user, display_name: str, avatar_url: str):
    '''Generates the embed for account info of a user.'''

    content = UserInfoContent(user, display_name)

    embed = nextcord.Embed()
    embed.title = content.info_title
    embed.description = content.info_description
    embed.color = nextcord.Color.purple()

    embed.add_field(name=content.field1['name'], value=content.field1['value'], inline=False)
    embed.add_field(name=content.subfield1_3['name'], value=content.subfield1_3['value'], inline=True)
    embed.add_field(name=content.subfield1_2['name'], value=content.subfield1_2['value'], inline=True)
    embed.add_field(name=content.subfield1_1['name'], value=content.subfield1_1['value'], inline=True)

    embed.add_field(name=content.field2['name'], value=content.field2['value'], inline=False)
    embed.add_field(name=content.field3['name'], value=content.field3['value'], inline=False)
    embed.add_field(name=content.field4['name'], value=content.field4['value'], inline=False)

    embed.set_thumbnail(url=avatar_url)
    embed.set_footer(text=content.info_footer)

    return embed


# Giveaway Embeds # #TODO# #TODO# #TODO#
def embed_giveaway(arg_lst: list):
    '''Generates the embed for a giveaway module.'''
    
    #content = GiveawayContent(arg_lst)

    embed = nextcord.Embed()
    #embed.title = content.title

    return embed


# Shuffle Embeds #
def embed_shuffle(collection: str, available: int, price: int, shuffle_type: str, url: str = None):
    '''Generates the embed for a shuffle module.'''

    content = ShuffleContent(collection, available, price, shuffle_type)

    embed = nextcord.Embed()
    embed.title = content.title
    embed.color = nextcord.Color.purple()
    
    embed.add_field(name=content.slots['name'], value=content.slots['value'], inline=True)
    embed.add_field(name=content.price['name'], value=content.price['value'], inline = True)
    embed.add_field(name=content.shuffle_type['name'], value=content.shuffle_type['value'], inline=True)
    embed.add_field(name=content.instructions['name'], value=content.instructions['value'], inline=False)
    embed.set_footer(text=content.footer)

    if url:
        embed.set_image(url=url)

    return embed

def embed_invalid_shuffle(collection: str, available: int, price: int, shuffle_type: str):

    content = ShuffleContent(collection, available, price, shuffle_type)

    embed = nextcord.Embed()
    embed.title = content.invalid_title
    embed.color = nextcord.Color.red()

    embed.add_field(name=content.invalid_collection['name'], value=content.invalid_collection['value'], inline=True)
    embed.add_field(name=content.invalid_shuffle_type['name'], value=content.invalid_shuffle_type['value'], inline=True)
    embed.set_footer(text=content.invalid_footer)

    return embed

def embed_shuffle_records(display_name: str, display_avatar: str, element_id: int, user_entries: list):

    content = ShuffleUserRecordsContent(display_name, element_id, user_entries)

    embed = nextcord.Embed()
    embed.title = content.title
    embed.description = content.description
    embed.color = nextcord.Color.purple()

    embed.add_field(name=content.entries['name'], value=content.entries['value'], inline=False)
    embed.set_footer(text=content.footer)
    embed.set_thumbnail(url=display_avatar)

    return embed

def embed_payment(price: int):

    content = ShufflePaymentContent(price)

    embed = nextcord.Embed()
    embed.title = content.title
    embed.description = content.description
    embed.color = nextcord.Color.purple()

    embed.add_field(name='Target Wallet', value=f'`{FINANCIAL_ADDRESS}`')
    
    return embed

def embed_unsuccesful_pay(interaction_id: int):
    '''Generates the embed for an unsuccessful shuffle entry payment.'''

    embed = nextcord.Embed()
    embed.title = f'Shuffle Entry ID: `{interaction_id}`'
    embed.description = 'Your transaction was not found or the transaction was incomplete! Please enter again. If you have already paid, there is no need to pay again—just press the confirm button when prompted.'
    embed.color = nextcord.Color.red()

    return embed

def embed_successful_pay(interaction_id: int):
    '''Generates the embed for a successful shuffle entry payment.'''

    embed = nextcord.Embed()
    embed.title = f'Shuffle Entry ID: `{interaction_id}`'
    embed.description = 'Your shuffle was successfully recorded. Your product will be available in the claim portal when it is ready.'
    embed.color = nextcord.Color.green()

    return embed


# Claim Embeds #

def embed_claim():
    '''Generates the embed for the claim portal.'''

    content = ClaimContent()

    embed = nextcord.Embed()
    embed.title = content.title
    embed.description = content.description
    embed.color = nextcord.Color.purple()

    embed.add_field(name=content.field1['name'], value=content.field1['value'])
    embed.set_footer(text=content.footer)

    return embed

def embed_claim_confirm(claimable_assets: list):
    '''Generates the embed for the claim distribution process'''

    content = embed_claim_confirm(claimable_assets)

    embed = nextcord.Embed()
    embed.title = content.title
    embed.description = content.description
    embed.color = nextcord.Color.purple()

    embed.add_field(name=content.assets['name'], value=content.assets['value'])
    embed.set_footer(text=content.footer)

    return embed