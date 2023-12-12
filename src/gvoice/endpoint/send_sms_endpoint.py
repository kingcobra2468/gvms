import random
import time
import logging

import requests

from gvoice.endpoint.base_endpoint import BaseEndpoint

logger = logging.getLogger(__name__)


class SendSMSEndpoint(BaseEndpoint):
    """Endpoint for sending a sms message to a recipient.
    """
    SMS_ENDPOINT = 'https://clients6.google.com/voice/v1/voiceclient/api2thread/sendsms'

    def __init__(self, cookies, gvoice_key, phone_number):
        super().__init__(cookies, gvoice_key, phone_number)

    def send_sms(self, phone_number, message):
        """Sends a sms message to a given recipient. 

        Args:
            phone_number (str): phone number of the recipient.
            message (str): message contents to send.
        """
        current_time = self.__get_current_milli_time()
        msg_send_time = 0

        # check if message id has been used before. Keep trying to send it under
        # new random message id until success.
        while msg_send_time < current_time:
            msg_send_time = self._send_sms(phone_number, message)

    def _send_sms(self, phone_number, message):
        """Sends a sms message to a given recipient. 

        Args:
            phone_number (str): phone number of the recipient.
            message (str): message contents to send.

        Raises:
            ValueError: raised if non 200 HTTP code observed.

        Returns:
            int: timestamp, in second, when the message was sent.
        """
        msg_id = self._gen_msg_id()
        resp = requests.post(self.SMS_ENDPOINT, headers=self.HEADERS, allow_redirects=True, params={'key': self._gvoice_key, 'alt': 'protojson'},
                             data=f'[null,null,null,null,"{message}",null,["+{phone_number}"],null,[{msg_id}]]')

        if resp.status_code != requests.codes.unauthorized:
            raise ValueError(
                'Unauthorized access due to expired or invalid cookies')

        if resp.status_code != requests.codes.ok:
            logger.error(
                f'List API failed and returned code {resp.status_code} with msg:\n {resp.text}.')
            raise ValueError(
                f'List API failed and returned code {resp.status_code} with msg:\n {resp.text}\n')

        data = resp.json()

        return data[3]

    def _gen_msg_id(self):
        """Generates a random message id.

        Returns:
            int: message id.
        """
        msg_id = random.randint(1, 10000000)

        return msg_id

    def _get_raw_data(self, num_records, **kwargs):
        pass

    def _parse_data(self, data):
        pass

    def __get_current_milli_time(self):
        """Gets the current time in milliseconds.

        Returns:
            int: time in milliseconds.
        """
        return round(time.time() * 1000)
