### User Utils ###

### Imports ###

# General
import datetime
import asyncio

# Library
import traceback
import requests
from tinydb import TinyDB, Query

# Internal
from utils.apis import RequestEndpoints
import utils.content as c

# Constant defining.
MEJIBASE_PATH = 'databases/mejibase.json'
CREATOR_WALLETS = {
    'MesiSols': 'OXQV2PS5LY7XMIRA3DYWQ7ZJW2AYQHTUANXOWZPC5ZQYGGPNM3PQJOYSDI'
}


class User():
    '''A class used for initializing key data from a user given only their id.'''

    def __init__(self, user_id: int):
        self.user_id = user_id

        # Define the central database and query method for users.
        self.db = TinyDB(MEJIBASE_PATH)
        self.Query = Query()

        # Make the user's data easily accessible as attributes.
        user_dict = self.db.search(self.Query.user_id == user_id)[0]
        self.wallets = user_dict['wallets']
        self.collections = user_dict['collections']
        self.assets = user_dict['assets']
        self.affiliation = user_dict['affiliation']
        try:
            self.claimable = user_dict['claimable']
        except KeyError:
            self.claimable = []
    
    def add_wallet(self, wallet_address: str):
        '''Method for updating a user's wallets in the database.'''
        self.wallets.append(wallet_address)
        self.db.update({'wallets': self.wallets}, self.Query.user_id == self.user_id)
    
    async def verify_assets(self):
        '''Method for obtaining what collections a user owns.'''

        verified_collections = []
        endpoint = RequestEndpoints().endpoint
        
        try:
            for wallet in self.wallets:
                wallet_request_url = f'{endpoint}/v2/accounts/{wallet}'
                account = requests.get(wallet_request_url).json()
                assets = account['account']['assets']

                for asset in assets:
                    asset_request_url = f'{endpoint}/v2/assets/{asset["asset-id"]}'
                    asset_info = requests.get(asset_request_url).json()['asset']
                    asset_creator = asset_info['params']['creator']
                    asset_id = asset_info['index']

                    for collection, creator_address in CREATOR_WALLETS.items():
                        if asset_creator == creator_address:
                            self.assets.append(asset_id)
                            self.collections.append(collection)
                            verified_collections.append(collection)
        except (ValueError, KeyError):
            traceback.print_exc()
            return False
        
        # Ensure no duplicates.
        collection_set = set(self.collections)
        collection_lst = list(collection_set)
        self.collections = collection_lst

        asset_set = set(self.assets)
        asset_lst = list(asset_set)
        self.assets = asset_lst
        
        self.db.update({'collections': self.collections, 'assets': self.assets}, self.Query.user_id == self.user_id)
        return verified_collections
    
    def unlink(self):
        '''Method for unlinking a user from the database.'''
        self.db.remove(self.Query.user_id == self.user_id)

    async def checktxns(self, hours: int, amount: int, purpose: str, specific_wallet: str=None, checks: int=10):
        '''
        Method for checking to see if there is a valid txn 
        from the user given some parameters.
        '''

        address_check = False

        # Define some parameters for the request.
        time = datetime.date.today() - datetime.timedelta(hours=hours)
        endpoint = RequestEndpoints().endpoint

        # Let Meji check a certain amount of times for the txn; defaults to 10.
        for _ in range(checks):
            if not specific_wallet:
                for wallet in self.wallets:
                    # Define url for checking payment txns in the timeframe
                    url = f'{endpoint}/v2/accounts/{wallet}/transactions?tx-type=pay&after-time={time}'
                    response = requests.get(url=url)
                    txns = response.json()['transactions']
                    address_check = self.checkaddress(wallet, txns, amount, purpose)

                    if address_check:
                        break
            else:
                url = f'{endpoint}/v2/accounts/{specific_wallet}/transactions?tx-type=pay&after-time={time}'
                response = requests.get(url=url)
                txns = response.json()['transactions']
                address_check = self.checkaddress(specific_wallet, txns, amount, purpose)
            
            await asyncio.sleep(3)

        return address_check

    def checkaddress(self, address: str, txns: list, amount: int, purpose: str):
        '''
        Submethod for checking for a valid txn from just one wallet.
        '''

        txn_db = TinyDB(c.txnbase_path)
        Txn = Query()

        for txn in txns:
            receiver = txn['payment-transaction']['receiver']
            pay_amount = int(txn['payment-transaction']['amount'])
            id = txn['id']

            if receiver == c.FINANCIAL_ADDRESS and pay_amount >= amount and not txn_db.contains(Txn.txn_id == id):
                txn_db.insert({'txn_id': id, 'sender': address, 'amount': amount, 'purpose': purpose})
                return True
            else:
                continue
        
        return False



