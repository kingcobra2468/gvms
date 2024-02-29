import logging

from gvoice.endpoint.base_endpoint import BaseEndpoint
from driver.chrome import GVoiceChromeDriver

logger = logging.getLogger(__name__)


class SendSMSEndpoint():
    """Endpoint for sending a sms message to a recipient.
    """

    def __init__(self, cookies, gvoice_key, phone_number):
        self._cookies = cookies
        self._gvoice_key = gvoice_key
        self._phone_number = phone_number

    def send_sms(self, phone_number, message):
        """Sends a sms message to a given recipient. 

        Args:
            phone_number (str): phone number of the recipient.
            message (str): message contents to send.
        """
        gvoice_chrome_driver = GVoiceChromeDriver()
        gvoice_chrome_driver.load_cookies(self._cookies)
        gvoice_chrome_driver.send_sms(phone_number, message)
        gvoice_chrome_driver.close()
