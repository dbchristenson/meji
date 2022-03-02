# Imports #

# General
from random import choice

# Library
import nextcord

# Internal
import utils.user as m_user


# General Content #
mejibase_path = 'databases/mejibase.json'
txnbase_path = 'databases/txns.json'
error_timeout = 'My internal clock has noticed that you have taken too long to respond. Please try again.'
error_internal = 'An internal error has occured. Please try again—if the problem persists please notify the MesiTeam, thank you!'
error_explorer = 'We failed to receive a response from AlgoExplorer, please try again shortly.'

FINANCIAL_ADDRESS = 'MESIH4234BEY5ENN6TGKN4YGALXSLYGM5P6CBUSENNSCGRQUWBB432Y33E'

# Data #
creator_wallets = {
    'MesiSols': 'OXQV2PS5LY7XMIRA3DYWQ7ZJW2AYQHTUANXOWZPC5ZQYGGPNM3PQJOYSDI'
}
collection_roles = {
    'MesiSols': 938642564825878601,     # This links to the Mesinaught role which may be confusing.
    'Eryan': 938563423036403752,        # This are the roles for the actual Mesinaught collection b/c
    'Sydian': 938563662430486529,       # there are different races to connect.
    'Mejadi': 938563684802908191
}


# Debrief Content #
class DebriefContent():
    def __init__(self):
        self.title = 'Looks like you just stepped into the Mesiverse!'
        self.description = 'The MesiStation is glad to have more hands, Cadet. 🤝'
        self.url = 'https://cdn.discordapp.com/attachments/883461718959857726/938875227440574555/2000x400_banner.png'
        self.field1 = ({
            'name': '**❏ What is Mesiverse? 🌌**',
            'value': ">>> Mesiverse is an organization of creators on the Algorand Blockchain. Mesiverse aspires to develop open-source blockchain software on top of a cohesive, lore-filled collection of NFTs set in the Mesiverse."
        })
        self.field2 = ({
            'name': '**❏ Our Mission Statement 🧩**',
            'value': (">>> Our aim is for NFT culture to shift to a more sustainable environment by building on Algorand. "
                    "Algorand's carbon negative status makes it perfect to launch ecologically responsible collections on. "
                    "Mesiverse seeks to expand Algorand's goal by putting aside 20% of revenue to donate to the **International "
                    "Dark Sky Association (IDA)** and the **Save the Boundary Waters Campaign (SBWC)**, a National Park recognized "
                    "by the IDA as a Dark Sky Sanctuary that is under threat of losing land to mining operations and other "
                    "intrusive developments.")
        })
        self.field3 = ({
            'name': '**❏ Why we decided on Algorand 🌳**',
            'value': (">>> Aside from Algorand's status as a carbon negative blockchain, the MesiTeam also chose Algorand for "
                    "other reasons. A huge part of our decision to use Algorand is its developer-friendly nature and we are "
                    "glad to be contributing to Algorand's rapid growth as it moves its way to becoming the blockchain of the future.")
        })
        self.field4 = ({
            'name': '**❏ Our Imminent Plans 🕙**',
            'value': (">>> The MesiTeam has been hard at work at developing the fundamentals for our project. We hope to release " 
                    "three collections this year which will make up the first season of Mesivere lore. On top of that, we plan "
                    "to develop useful software for other creators who are seeking to upgrade their community's experience through "
                    "open-source software and possibly licensing for smart contracts, asset creation, and Discord bots—like Meji!")
        })
        self.footer = 'The MesiTeam would like to thank you for looking at our project. We encourage you to stay and monitor or discuss the project whether you are currently interested in purchasing or not.'


# Regulations Content #
class RegulationContent():
    def __init__(self):
        self.title = 'MesiStation Regulations 📚'
        self.description = ("All members of the MesiStation are expected to comply with "
                            "**[Discord's TOS](https://discord.com/terms)** as well as our **own "
                            "bylaws.** Investigated personnel found breaking these rules will "
                            "be subject to displinary action and **eventual removal after "
                            "repeat offenses** have been made or if the MesiTeam determines "
                            "the offense to be too severe to allow.")
        self.field1 = ({
            'name': '**❏ Rule #1: Practice Respect**',
            'value': '>>> Be amicable with your peers regardless of your personal feelings. More serious offenses such as hate speech, threats, and bullying are subject to instant removal.'
        })

        self.field2 = ({
            'name': '**❏ Rule #2: Responsible Messaging**',
            'value': '>>> Cadets must refrain from polluting the server with spam and avoid disturbing their peers through pings. Soliciting is only allowed under **express permission** from the MesiTeam. Please also refrain from discussing and sharing fringe or taboo topics.'
        })

        self.field3 = ({
            'name': '**❏ Rule #3: Member Privacy**',
            'value': '>>> Do not directly message other members without purpose. Do not expose any sensitive information regarding yourself or other members of the MesiStation.'
        })

        self.field4 = ({
            'name': '**❏ Rule #4: Appropriate Judgement**',
            'value': '>>> Please use your best discretion when interacting with the MesiStation. The MesiStation is meant to observe a generally positive sentiment, unnecessarily negative dialogue is heavily discouraged. Negative dialogue targeted at other projects will be met with a mute—we do not tolerate targeted FUD against adjacent projects.'
        })


# Connections Content #
class ConnectionsContent():
    def __init__(self):
        self.title = 'Discover Mesiverse on the Web 🔗'
        self.description = 'Browse links to official Mesiverse social media outlets, our verified collections pages, github, and more when visiting our website!'
        self.footer = 'The MesiTeam would like to thank you for looking at our project. We encourage you to stay and monitor or discuss the project whether you are currently interested in purchasing or not.'
        self.url = 'https://cdn.discordapp.com/attachments/938581646096081056/938639598966423592/sol_only_9.png'
        self.link1 = {
            'label': 'Mesiverse.org',
            'url': 'https://www.mesiverse.org',
            'emoji': nextcord.PartialEmoji.from_str('<:mesiverselogo:938646432267784193>')
        }
        self.link2 = {
            'label': 'Explorer',
            'url': 'https://www.nftexplorer.app/collection/mesisols',
            'emoji': nextcord.PartialEmoji.from_str('<:nftexplorerlogo:938646432141946950>')
        }
        self.link3 = {
            'label': 'Twitter',
            'url': 'https://twitter.com/mesiverse',
            'emoji': nextcord.PartialEmoji.from_str('<:twitterlogo:938646432318128248>')
        }
        self.link4 = {
            'label': 'Git',
            'url': 'https://github.com/dbchristenson',
            'emoji': nextcord.PartialEmoji.from_str('<:githublogo:938646432397791362>')
        }


# Orientation Content
class OrientationContent():
    def __init__(self):
        self.title = 'Welcome aboard the MesiStation!'
        self.description = 'I am Meji, the Mejadi tasked with keeping the station operational. To gain access to other parts of the station, press the button below and become a certified MesiCadet today!'
        self.thumbnail_url = 'https://cdn.discordapp.com/attachments/915079764073664542/937556734321500180/mejibot2.png'

        self.already_registered = 'You are already a cadet in our system.'
        self.successfully_registered = 'Your registration was successful. Feel free to explore the MesiStation and we look forward to having you with us, cadet!'


# Registrar Content
class RegistrarContent():
    def __init__(self):
        self.title = '**MesiStation Registrar **'
        self.description = ('Want to participate in giveaways? Verify your *shiny* new Mesiverse NFT? '
                            'Maybe a chance for some airdrops? Do not miss out! Configure your account '
                            'with the registrar today!')
        self.field1 = {'name': '**❏ Wallet Linking** 📟',
                        'value': '>>> Meji will direct message the user and ask for their wallet address to '
                                'ensure privacy. After receiving it, Meji will prompt the user to send a 0 Algo '
                                'transaction to a target wallet address to confirm account ownership.'
                        }
        self.field2 = {'name': '**❏ Asset Verification** 🚀',
                        'value': ">>> Meji will search through each wallet linked to the user and update the user's roles appropriately."
                        }
        self.field3 = {'name': '**❏ Account Unlinking** 🧨',
                        'value': '>>> Meji will erase all data tied to the user from the database and '
                                'relenquish any roles that the user has received other than their '
                                'status as a cadet.'
                        }
        self.field4 = {'name': '**❏ Account Info** 🔎',
                        'value': '>>> Meji will reply with a report of information about your account such as '
                                'what wallets are currently linked to your account, what asset ids are currently '
                                'registered to you, and more.'
                        }
        self.url = ''
        self.footer = ('The unlinking process removes your entire account from our databases '
                        'and will wipe all the roles you hold on the MesiStation. Please be '
                        'sure you desire this outcome before proceeding. If you experience '
                        'any issues with the registrar, please notify the MesiTeam.')
        
        self.wallet_title = choice(["Let's get you hooked up! 🪝", "Ready to get linked? ⛓", "At your service, cadet! 👟"])
        self.wallet_description = 'Please paste the address of the wallet you would like to add to your account into the chat below.'
        self.wallet_footer = ''
        self.wallet_used = 'You have already linked this wallet to your account or it is an invalid address!'

        self.upd_wallet_title = choice(["Thanks! time to verify it's yours!", "Thanks! I just gotta make sure this is your's first!"])
        self.upd_wallet_description = ('Just send a **0 Algo** transaction to the wallet below, **press the confirm button below** and when the '
                                        'transaction has been confirmed, your new wallet address will be linked right away! **Make sure you '
                                        'are using your selected wallet:** ')

        self.completed_wallet_title = 'Wallet Link Interaction ID: '

        self.success_link = ('Your wallet address has been linked to your account and can now be used for in shuffles, '
                            'giveaways, airdrops, asset verification, and more!')
        self.success_unlink = ('Your account has been successfully unlinked and your roles have been relinquished. '
                                'You must go through orientation again to access the MesiStation.')
        self.success_verify_assets = ('Your linked wallets have been checked for Mesiverse assets and your roles '
                                    'have been updated accordingly. If you believe there was a mistake, please check '
                                    'that your linked wallets or contact the MesiTeam to report a bug. Thank you for '
                                    'supportin the Mesiverse!')
        self.permission_failure = 'Sorry, I do not possess the correct permissions to perform that'
        self.failure_link = 'The wallet linking process has failed, please try again and ensure you have followed the correct steps.'
        self.failure_link_reasons = ('The process may have failed because of an invalid wallet address or because we did not receive '
                                'your transaction. Please try again or contact the MesiTeam if you believe this is a bug.')
        
        self.success_link_reply = 'Success! Your wallet has been linked to the MesiStation!'
        self.failure_link_reply = 'The wallet linking process has failed.'

class UserInfoContent():
    def __init__(self, user: m_user.User, display_name: str):
        self.info_title = f'Database Entry: `@{display_name}`'
        self.info_description = 'Here is the brief of the account. Some data may be pruned to maintain privacy for members of the MesiStation.'

        # General Field
        self.field1 = {
            'name': '**❏ General Information**',
            'value': 'General information about the account of the member—mostly minor details for administration purposes.'
        }
        self.subfield1_3 = {
            'name': 'User ID',
            'value': f'`{user.user_id}`'
        }
        self.subfield1_2 = {
            'name': 'MesiNFTs',
            'value': f'`{len(user.assets)} Asset(s)`'
        }
        self.subfield1_1 = {
            'name': 'Affiliation',
            'value': f'`{user.affiliation}`'
        }

        # Wallet Field
        wallets_lst = []
        for wallet in user.wallets:
            emoji = nextcord.PartialEmoji.from_str('<:offline:903340437471899679>')
            wallets_lst.append(f'{emoji} `{wallet[:6]} ...`')
        
        if not wallets_lst:
            wallets_lst = ['No linked wallets detected.']

        self.field2 = {
            'name': '**❏ Linked Wallets**',
            'value':  '\n'.join(wallets_lst)
        }
        # Collections Field
        self.field3 = {
            'name': '**❏ Collections**',
            'value': '>>> ' + ', '.join(user.collections)
        }
        # Assets Field
        self.field4 = {
            'name': '**❏ Assets**',
            'value': '>>> ' + ', '.join([f'`{str(asset)}`' for asset in user.assets[:50]])
        }

        self.info_footer = 'If your information is incorrect make sure to re-verify your assets and check your wallet addresses or contact the MesiTeam to report a bug.'
        

# Shuffle Content
class ShuffleContent():
    def __init__(self, collection: str, available: int, price: int, shuffle_type: str):
        self.title = f'A Shuffle for {collection.upper()} is Occuring!'
        self.slots = {
            'name': 'Total Slots 👥',
            'value': f'**{available} Available**'
        }
        self.price = {
            'name': 'Entry Price 🏷',
            'value': f'**{price} Algo**'
        }
        self.shuffle_type = {
            'name': 'Distribution 🚚',
            'value': f'**{shuffle_type}**'
        }
        self.instructions = {
            'name': '**❏ Instructions**',
            'value': ('>>> **1.** Use the enter button to begin the entry process\n'
                          '**2.** Pay the entry fee after prompted by Meji\n'
                          '**3.** Once the payment is confirmed on the blockchain, confirm with Meji\n'
                          '**4.** Your NFT will become claimable according to the distribution type')
        }
        self.footer = 'Built by the MesiTeam. If you encounter an error or bug please contact us!'

        self.invalid_title = 'This Shuffle is no Longer Accepting Entries'
        self.invalid_collection = {
            'name': 'Related Collection',
            'value': f'`{collection.upper()}`'
        }
        self.invalid_shuffle_type = {
            'name': 'Shuffle Type',
            'value': f'`{shuffle_type.upper()}`'
        }
        self.invalid_footer = 'Built by the MesiTeam'

        self.successful_entry = 'You have been entered into the shuffle. Press the records button to confirm your entry.'
        self.unsuccessful_entry = 'Your shuffle entry has failed.'

class ShuffleUserRecordsContent():
    def __init__(self, display_name: str, element_id: int, user_entries: list):
        self.title = f'Shuffle Records: `@{display_name}`'
        self.description = f'Recorded Data for Shuffle `#{element_id}`'

        if not user_entries:
            formatted_entries = ['`No Entries Detected`']
        else:
            formatted_entries = [f'`{entry}`' for entry in user_entries]
        
        self.entries = {
            'name': '**❏ Recorded Entries**',
            'value': '>>> ' + '\n'.join(formatted_entries)
        }

        self.footer = 'If you believe this data is incorrect please contact the MesiTeam.'

class ShufflePaymentContent():
    def __init__(self, price: int):
        self.title = 'Shuffle Entry Portal'
        self.description = (f'To complete your entry, please send a **{price} Algo** payment from **A WALLET ALREADY LINKED TO YOUR ACCOUNT** '
                              'to the wallet below. **Press the confirm button** when the transaction has been confirmed. After Meji detects a '
                              'successful transaction, your entry will be validated.')


# Claim Content
class ClaimContent():
    def __init__(self):
        self.title = 'MesiStation Claiming Portal'
        self.description = 'Automatically claim any purchased or won assets using our state of the art claiming portal!'
        self.field1 = {
            'name': '**❏ Instructions**',
            'value': ('>>> **1.** Use the claim button to begin the process\n'
                      '**2.** Add the asset ids that Meji prompts you to\n'
                      '**3.** Notify Meji by confirming the assets have been opted in\n'
                      '**4.** Receive the assets to your wallet address')
            }
        self.footer = 'If you encounter any claiming errors please contact the MesiTeam.'

class ClaimConfirmContent():
    def __init__(self, claimable_assets: list):      
        title_choices = ['Thanks for finding a new home for these guys!', 
                         'Treat them well, the Mesiverse will miss them!', 
                         'Thanks for supporting the Mesiverse!',
                         'Ready for your shiny new NFTs?']
        self.title = choice(title_choices)
        self.description = 'Simply opt in to the assets below and click the button when you are done! Your NFTs will be on the way in no time.'
        self.assets = {
            'name': '**❏ Assets**',
            'value': '>>> ' + ', '.join([f'`{str(asset)}`' for asset in claimable_assets[:50]])
            }
        self.footer = 'You have 5 minutes to complete this process and press the confirmation button.'
        