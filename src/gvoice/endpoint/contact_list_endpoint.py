import requests

from gvoice.endpoint.base_endpoint import BaseEndpoint


class ContactListEndpoint(BaseEndpoint):
    """Endpoint for retrieving contact list of every recipient that this GVoice account
    has sent a message to.
    """
    LIST_CONTACTS_ENDPOINT = 'https://clients6.google.com/voice/v1/voiceclient/api2thread/list'

    def __init__(self, cookies, gvoice_key, phone_number):
        super().__init__(cookies, gvoice_key, phone_number)

    def get_contact_list(self):
        """Retrieves the complete list of all known recipients.

        Returns:
            list(str): list of numbers of all of the recipients.
        """
        contact_list = self._get_complete_set()

        contact_list = [contact[0].strip('t.+') for contact in contact_list]
        # remote all group messages
        # TODO: implement logic for handling group messages
        contact_list = list(
            filter(lambda contact: 'g.Group' not in contact, contact_list))

        return contact_list

    def _get_raw_data(self, num_records, **kwargs):
        resp = requests.post(self.LIST_CONTACTS_ENDPOINT, headers=self.HEADERS, allow_redirects=True, params={'key': self._gvoice_key, 'alt': 'protojson'},
                             data=f'[2,{num_records},1,null,null,[null,true,true]]')

        return resp

    def _parse_data(self, data):
        return data[0]
