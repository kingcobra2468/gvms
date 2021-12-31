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
            cookies = secrets['cookies']

            if 'SAPISID' not in cookies.keys():
                raise ValueError(
                    'SAPISID cookie is missing from the list of available cookies')

            self.__prase_cookies(cookies)

    def __prase_cookies(self, cookies):
        cookie_terms = []
        for cookie in cookies:
            cookie_terms.append((f'{cookie["name"]}={cookie["value"]}'))
