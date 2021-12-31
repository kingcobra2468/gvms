import random

import requests

from util.auth import gen_auth_code


class Account:
    SMS_ENDPOINT = 'https://clients6.google.com/voice/v1/voiceclient/api2thread/sendsms'
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

        self.HEADERS['Authorization'] = f'SAPISIDHASH {gen_auth_code(sapisid)}'
        self.HEADERS['Cookie'] = cookies

    def get_known_recipients(self):
        pass

    def send_sms(self, recipient, message):
        msg_id = random.randint(1, 10000000)
        print(self.HEADERS)
        r = requests.post(self.SMS_ENDPOINT, headers=self.HEADERS, allow_redirects=True, params={'key': self._gvoice_key, 'alt': 'protojson'},
                          data=f'[null,null,null,null,"{message}",null,["+{recipient}"],null,[{msg_id}]]')
        print(r.status_code, r.json())

    def get_recipient_history(self):
        pass

    def get_known_recipients(self):
        pass
