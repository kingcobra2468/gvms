from abc import ABC, abstractmethod
from time import sleep

import requests

from util.auth import gen_auth_code
from util.sequence import exp_sequence


class BaseEndpoint(ABC):
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
        self._cookies = cookies
        self._gvoice_key = gvoice_key
        self._phone_number = phone_number

        self.HEADERS['Authorization'] = f'SAPISIDHASH {gen_auth_code(self._cookies["SAPISID"])}'
        self.HEADERS['Cookie'] = self.__encode_cookies(self._cookies)

    def __encode_cookies(self, cookies):
        cookie_terms = []

        for cookie_name, cookie_value in cookies.items():
            cookie_terms.append(f'{cookie_name}={cookie_value}')
        encoded_cookies = '; '.join(cookie_terms)

        return encoded_cookies

    def _get_complete_set(self):
        data = None
        num_records_prev_actual = 0

        for num_records_pred in exp_sequence():
            resp = self._get_data(num_records_pred)

            if resp.status_code != requests.codes.ok:
                raise ValueError(
                    f'List API failed and returned code {resp.status_code} with msg:\n {resp.text}\n')

            raw_data = resp.json()
            data = self._parse_data(raw_data)
            num_contacts_actual = len(data)
            if num_records_prev_actual == num_contacts_actual:
                break

            num_records_prev_actual = num_contacts_actual
            sleep(0.5)

        return data

    @abstractmethod
    def _get_data(self, num_records):
        pass

    @abstractmethod
    def _parse_data(self, data):
        pass
