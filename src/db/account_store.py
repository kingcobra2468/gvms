from gvoice.account.account import Account
import os.path
import glob
import json


class AccountStore:
    def __init__(self, secrets_dir):
        self._secrets_glob = os.path.join(secrets_dir, 'secrets_*.json')
        self._accounts = {}

    def load_accounts(self):
        accounts_secrets = glob.glob(self._secrets_glob)
        for account in accounts_secrets:
            secrets = json.load(open(account, 'r'))

            phone_number = secrets['phone_number']
            gvoice_key = secrets['gvoice_key']
            cookies = secrets.get('cookies', dict())
            cookies = self.__prase_cookies(cookies)
                        
            if 'SAPISID' not in cookies.keys():
                raise ValueError(
                    'SAPISID cookie is missing from the list of available cookies')
            
            self._accounts[phone_number] = Account(cookies, gvoice_key, phone_number)
    
    def get_account(self, phone_number):
        if phone_number not in self._accounts:
            return None
        
        return self._accounts[phone_number]
    
    def __prase_cookies(self, raw_cookies):
        cookies = dict()
        
        for cookie in raw_cookies:
            cookie_name= cookie["name"]
            cookie_value = cookie["value"]
            cookies[cookie_name] = cookie_value
            
        return cookies
    