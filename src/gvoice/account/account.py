from time import sleep
import random

import requests

from util.auth import gen_auth_code
from util.sequence import exp_sequence


class Account:
    SMS_ENDPOINT = 'https://clients6.google.com/voice/v1/voiceclient/api2thread/sendsms'
    LIST_CONTACTS_ENDPOINT = 'https://clients6.google.com/voice/v1/voiceclient/api2thread/list'
    LIST_MSGS_ENDPOINT = 'https://clients6.google.com/voice/v1/voiceclient/api2thread/get'
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

    def get_known_sms_recipients(self):
        pass

    def send_sms(self, recipient, message, safe_mode=False):
        msg_id = random.randint(1, 10000000)
        r = requests.post(self.SMS_ENDPOINT, headers=self.HEADERS, allow_redirects=True, params={'key': self._gvoice_key, 'alt': 'protojson'},
                          data=f'[null,null,null,null,"{message}",null,["+{recipient}"],null,[{msg_id}]]')
        print(r.status_code, r.json())

    def get_recipient_sms_history(self):
        pass

    def get_known_recipients(self):
        self._get_complete_sms_set()

    def __encode_cookies(self, cookies):
        cookie_terms = []

        for cookie_name, cookie_value in cookies.items():
            cookie_terms.append(f'{cookie_name}={cookie_value}')
        encoded_cookies = '; '.join(cookie_terms)

        return encoded_cookies

    def _get_complete_sms_set(self):
        contact_data = []
        num_contacts_prev_actual = 0

        for num_contacts_pred in exp_sequence():

            resp = requests.post(self.LIST_CONTACTS_ENDPOINT, headers=self.HEADERS, allow_redirects=True, params={'key': self._gvoice_key, 'alt': 'protojson'},
                                 data=f'[2,{num_contacts_pred},1,null,null,[null,true,true]]')
            if resp.status_code != requests.codes.ok:
                raise ValueError(
                    f'List API failed and returned code {resp.status_code} with msg:\n {resp.text}\n')

            data = resp.json()
            num_contacts_actual = len(data[0])
            if num_contacts_prev_actual == num_contacts_actual:
                contact_data = data[0]
                break

            num_contacts_prev_actual = num_contacts_actual
            sleep(0.5)

        contact_list = [contact[0].strip('t.+') for contact in contact_data]
        contact_list = list(
            filter(lambda contact: 'g.Group' not in contact, contact_list))

        return contact_list
