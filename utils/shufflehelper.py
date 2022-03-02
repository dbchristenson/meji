### Shuffle Utils ###

### Imports ###

# Library
from typing import Collection
from tinydb import TinyDB, Query

# Constant defining.
SHUFFLES_PATH = 'databases/shuffles.json'


class ShuffleHelper():
    '''A class for initialzing a shuffle obj that helps perform shuffle operations.'''

    def __init__(self, element_id: int):
        self.id = element_id

        # Grab relevant data from shuffle database.
        self.db = TinyDB(SHUFFLES_PATH)
        self.Shuffle = Query()

        self.data = self.db.search(self.Shuffle.id == self.id)[0]
        self.collection = self.data['collection']
        self.available = self.data['available']
        self.remaining = self.data['remaining']
        self.price = self.data['price']
        self.shuffle_type = self.data['shuffle_type']
        self.assets = sorted(self.data['assets'])
        self.entries = sorted(self.data['entries'])

    def get_entries(self, user_id: int):
        '''Get the entry data of entries from the given user_id.'''

        entry_ids = []

        for key, val in self.entries.items():
            if val == user_id:
                entry_ids.append(val[''])
        
        return entry_ids

    def add_assets(self):
        '''Method for adding assets to a shuffle.'''

        # Initalize relevant collection data.
        collection_db = TinyDB(f'databases/{self.collection}.json')
        Collection = Query()
        
        # Get list of useable assets and format in order of code.
        available_assets = collection_db.search(Collection.used_in_shuffle == False and Collection.owned == True)
        intermediate_assets = [(asset_dict['asset_code'], asset_dict) for asset_dict in available_assets]
        intermediate_assets.sort()
        assets_to_add = int(self.available)
        formatted_assets = [asset_dict for (_, asset_dict) in intermediate_assets[:assets_to_add]]

        # Add each asset in the range of assets to add to the shuffle.
        for asset in formatted_assets:
            asset['used_in_shuffle'] = True
            asset['assigned'] = False
            collection_db.update({'used_in_shuffle': True}, Collection.asset_id == asset['asset_id'])
            self.assets.append(asset)
        
        self.db.update({'assets': self.assets}, self.Shuffle.id == self.id)
    
    def decrement_shuffle(self):
        '''Method for decrementing the shuffle once entered.'''
        updated_remaining = int(self.remaining) - 1

        if updated_remaining == 0:
            updated_remaining = self.shutdown()
            self.db.update({'remaining': updated_remaining}, self.Shuffle.id == self.id)
            return updated_remaining
        else:
            self.db.update({'remaining': updated_remaining}, self.Shuffle.id == self.id)
            return updated_remaining
    
    def shutdown(self):
        '''Method for making a shuffle dormant.'''

        self.db.upsert({'active': False}, self.Shuffle.id == self.id)
        return 0





