### API Utils ###

### Imports ###

# General
import os

# Library
import requests

# Constant Defining
# Purestake requires authentication before accessing their API.
PURESTAKE_KEY = os.environ.get('PURESTAKE_KEY')
PURESTAKE_AUTH_HEADER = {'X-API-Key': PURESTAKE_KEY}


class RequestEndpoints():
    '''This is class for dynamically changing request urls if the main api service is down.'''
    def __init__(self):
        self.explorer_health = requests.get('https://algoindexer.algoexplorerapi.io/health').status_code
        self.purestake_health = requests.get('https://testnet-algorand.api.purestake.io/idx2/health', headers=PURESTAKE_AUTH_HEADER).status_code

        self.service = None
        self.endpoint = None

        self.default_service = 'Explorer'
        self.default_endpoint = 'https://algoindexer.algoexplorerapi.io'
        self.check_service()
    
    def check_service(self):
        '''Defines which service to use for requests.'''
        if not self.explorer_health != 200:
            self.service = 'Explorer'
            self.endpoint = 'https://algoindexer.algoexplorerapi.io'
        elif not self.purestake_health != 200:
            self.service = 'Purestake'
            self.endpoint = 'https://testnet-algorand.api.purestake.io/idx2'
        else:
            self.service = self.default_service
            self.endpoint = self.default_endpoint
