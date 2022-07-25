import os.path
import glob
import json
import logging

from gvoice.account.account import Account

logger = logging.getLogger(__name__)


class AccountStore:
    """Account store for managing known GVoice secrets.
    """
    instance = None

    def __init__(self, secrets_dir):
        """Constructor.

        Args:
            secrets_dir (str): directory where secrets are stored
        """
        self._secrets_glob = os.path.join(secrets_dir, 'secrets_*.json')
        self._accounts = {}

    @classmethod
    def get_instance(cls, secrets_dir=None):
        """Returns the singleton instance and creates new instance if none created
        yet.

        Args:
            secrets_dir (str): directory where secrets are stored
        """
        if not AccountStore.instance:
            AccountStore.instance = AccountStore(secrets_dir)

        return AccountStore.instance

    def load_accounts(self):
        """Parses secrets from the specified directory and loads them
        into memory.

        Raises:
            ValueError: raised if sapisid cookie in missing.
        """
        accounts_secrets = glob.glob(self._secrets_glob)
        for account in accounts_secrets:
            secrets = json.load(open(account, 'r'))

            phone_number = secrets['phone_number']
            gvoice_key = secrets['gvoice_key']
            cookies = secrets.get('cookies', dict())
            cookies = self.__prase_cookies(cookies)

            logger.info(f'Added new account for number {phone_number}.')
            # cookie needs to exist as it is critical for authorization
            if 'SAPISID' not in cookies.keys():
                raise ValueError(
                    'SAPISID cookie is missing from the list of available cookies')

            self._accounts[phone_number] = Account(
                cookies, gvoice_key, phone_number)

    def get_all_numbers(self):
        """Fetches all the GVoice numbers that are available in the cache.

        Returns:
            list(str): list of all of the GVoice numbers
        """
        return self._accounts.keys()

    def get_account(self, phone_number):
        """Retrieves the secrets for a given account.

        Args:
            phone_number (str): the GVoice phone number of the account.

        Returns:
            Account|None: account containing the secrets or None if the account doesn't exist.
        """
        if phone_number not in self._accounts:
            return None

        return self._accounts[phone_number]

    def __prase_cookies(self, raw_cookies):
        """Parses the cookies via the removal of all unnecessary metadata and restructures the 
        cookies as a key value attribute pair.

        Args:
            raw_cookies list(dict)): cookie dict as it exists in the secrets file.

        Returns:
            dict(): cookies as a key value attribute pair
        """
        cookies = dict()

        for cookie in raw_cookies:
            cookie_name = cookie["name"]
            cookie_value = cookie["value"]
            cookies[cookie_name] = cookie_value

        return cookies
