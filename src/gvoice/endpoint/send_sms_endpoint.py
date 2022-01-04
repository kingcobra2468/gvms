from gvoice.endpoint.base_endpoint import BaseEndpoint
import random
import requests
import time


class SendSMSEndpoint(BaseEndpoint):
    SMS_ENDPOINT = 'https://clients6.google.com/voice/v1/voiceclient/api2thread/sendsms'

    def __init__(self, cookies, gvoice_key, phone_number):
        super().__init__(cookies, gvoice_key, phone_number)

    def send_sms(self, phone_number, message):
        current_time = self.__get_current_milli_time()
        msg_send_time = 0

        while msg_send_time < current_time:
            msg_send_time = self._send_sms(phone_number, message)

    def _send_sms(self, phone_number, message):
        msg_id = self._gen_msg_id()
        resp = requests.post(self.SMS_ENDPOINT, headers=self.HEADERS, allow_redirects=True, params={'key': self._gvoice_key, 'alt': 'protojson'},
                             data=f'[null,null,null,null,"{message}",null,["+{phone_number}"],null,[{msg_id}]]')

        if resp.status_code != requests.codes.ok:
            raise ValueError(
                f'List API failed and returned code {resp.status_code} with msg:\n {resp.text}\n')

        data = resp.json()

        return data[3]

    def _gen_msg_id(self):
        msg_id = random.randint(1, 10000000)

        return msg_id

    def _get_data(self, num_records, **kwargs):
        pass

    def _parse_data(self, data):
        pass

    def __get_current_milli_time(self):
        return round(time.time() * 1000)
