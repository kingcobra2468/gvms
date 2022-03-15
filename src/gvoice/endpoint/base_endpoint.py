from abc import ABC, abstractmethod
from time import sleep

import requests

from util.auth import gen_auth_code
from util.sequence import exp_sequence


class BaseEndpoint(ABC):
    """Base class for building endpoint logic for GVoice APIs.
    """
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Goog-AuthUser': '0',
        'X-Requested-With': 'XMLHttpRequest',
        'X-JavaScript-User-Agent': 'google-api-javascript-client/1.1.0',
        'Content-Type': 'application/json+protobuf',
        'X-Origin': 'https://voice.google.com',
        'X-Referer': 'https://voice.google.com',
        'X-Goog-Encode-Response-If-Executable': 'base64',
        'Origin': 'https://clients6.google.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }

    def __init__(self, cookies, gvoice_key, phone_number):
        """Constructor.

        Args:
            cookies (dict()): all the cookies for a given GVoice account.
            gvoice_key (str): key as found in the query params.
            phone_number (str): phone number of the GVoice account. 
        """
        self._cookies = cookies
        self._gvoice_key = gvoice_key
        self._phone_number = phone_number

        self.HEADERS['Authorization'] = f'SAPISIDHASH {gen_auth_code(self._cookies["SAPISID"])}'
        self.HEADERS['Cookie'] = self.__encode_cookies(self._cookies)

    def __encode_cookies(self, cookies):
        """Encodes the cookies in the format that is used when sending cookies via
        the header.

        Args:
            cookies (dict()): all the cookies for a given GVoice account.

        Returns:
           str: cookies in the encoded form.
        """
        cookie_terms = []

        for cookie_name, cookie_value in cookies.items():
            cookie_terms.append(f'{cookie_name}={cookie_value}')
        encoded_cookies = '; '.join(cookie_terms)

        return encoded_cookies

    def _get_complete_set(self, **kwargs):
        """Fetches the full set of data records by sequentially guessing
        the number of messages by polling from an exponential sequence. Since
        there is no way to know the total number of data records, an increasing page
        prediction size will be used until the returned data's actual sizes is
        guessed.

        Example: There are 20 records in reality. The execution will be as follows:
        Guess 2; Returned 2
        Guess 4; Returned 4
        Guess 8; Returned 8
        Guess 16; Returned 16
        Guess 32: Returned 20
        Guess 64; Returned 20

        Since the last 2 page sizes both returned 20 records, it was determined that
        there are only 20 records available.

        Raises:
            ValueError: raised as a result when a non 200 HTTP code is observed.

        Returns:
            list(Any): data after going through the parser.
        """
        data = None
        num_records_prev_actual = 0

        for num_records_pred in exp_sequence():
            data = self._get_data(num_records_pred, **kwargs)
            num_contacts_actual = len(data)
            # last 2 iterations result in same number of records. Thus, max number of records has been
            # observed and all possible records have been retrieved.
            if num_records_prev_actual == num_contacts_actual:
                break

            num_records_prev_actual = num_contacts_actual
            sleep(0.5)

        return data

    def _get_data(self, num_records, **kwargs):
        """Fetches and applies the parser against the data.

        Args:
            num_records (int): 

        Raises:
            ValueError: number of records to retrieve.

        Returns:
            list(Any): data after going through the parser.
        """
        resp = self._get_raw_data(num_records, **kwargs)

        if resp.status_code != requests.codes.ok:
            raise ValueError(
                f'List API failed and returned code {resp.status_code} with msg:\n {resp.text}\n')

        data = resp.json()
        data = self._parse_data(data)
        
        return data
            
    @abstractmethod
    def _get_raw_data(self, num_records, **kwargs):
        """Abstract method to be implemented by the endpoint that will return the request's response
        of the endpoint.

        Args:
            num_records (int): number of records to retrieve.
        """
        pass

    @abstractmethod
    def _parse_data(self, data):
        """Abstract method to be implemented by the endpoint that will parse raw response data for
        useful data.  

        Args:
            data (list(Any)): list containing useful data from the response.
        """
        pass
