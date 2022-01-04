import requests

from gvoice.endpoint.base_endpoint import BaseEndpoint


class ContactHistoryEndpoint(BaseEndpoint):
    """Endpoint for retrieving sms history between the recipient and the
    GVoice account.
    """
    CONTACT_HISTORY_ENDPOINT = 'https://clients6.google.com/voice/v1/voiceclient/api2thread/get'

    def __init__(self, cookies, gvoice_key, phone_number):
        super().__init__(cookies, gvoice_key, phone_number)

    def get_contact_msg_history(self, phone_number):
        """Fetches the complete msg history between the recipient and the
        GVoice account. 

        Args:
            phone_number (str): recipient phone number.

        Returns:
            list(list(message_time, message,)): history of lists each of which contains the msg
            send/receive time in milliseconds, the message contents, and flag which if True means the message
            was send from the recipient and False if sent by the GVoice account. 
        """
        sms_history = []
        data = self._get_complete_set(phone_number=phone_number)

        for sms in data:
            message_time = sms[1]
            message = sms[9]
            # True if sent from contact and false if sent via us
            origin_contact = sms[17] is None

            sms_history.append([message_time, message, origin_contact])

        # remove all images sms messages from history
        sms_history = list(
            filter(lambda contact: 'MMS Sent' != contact[1] and 'MMS Received' != contact[1], sms_history))

        return sms_history

    def _get_data(self, num_records, phone_number):
        resp = requests.post(self.CONTACT_HISTORY_ENDPOINT, headers=self.HEADERS, allow_redirects=True, params={'key': self._gvoice_key, 'alt': 'protojson'},
                             data=f'["t.+{phone_number}",{num_records},null,[null,true,true]]')

        return resp

    def _parse_data(self, data):
        return data[0][2]
