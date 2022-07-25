import logging

from db.account_store import AccountStore
from gvoice.endpoint.send_sms_endpoint import SendSMSEndpoint
from gvoice.endpoint.contact_history_endpoint import ContactHistoryEndpoint
from gvoice.endpoint.contact_list_endpoint import ContactListEndpoint
from . import gvoice_pb2
from . import gvoice_pb2_grpc

logger = logging.getLogger(__name__)


class GVoiceHandler(gvoice_pb2_grpc.GVoiceServicer):

    def __init__(self):
        super().__init__()
        self._db = AccountStore.get_instance()

    async def SendSMS(self, request, context):
        account = self._db.get_account(request.gvoice_phone_number)
        if not account:
            return gvoice_pb2.SendSMSResponse(success=False, error='gvoice number doesn\'t exist')

        call = SendSMSEndpoint(
            account.cookies, account.gvoice_key, account.phone_number)
        try:
            call.send_sms(request.recipient_phone_number, request.message)
        except:
            logger.error(
                f'Unable to send sms to {request.recipient_phone_number} from {account.phone_number}.')
            return gvoice_pb2.SendSMSResponse(success=False, error='unable to process request')

        logger.info(f'Sent sms to {request.recipient_phone_number} from {account.phone_number}.')
        return gvoice_pb2.SendSMSResponse(success=True)

    async def GetContactList(self, request, context):
        account = self._db.get_account(request.gvoice_phone_number)
        if not account:
            return gvoice_pb2.FetchContactListResponse(success=False, error='gvoice number doesn\'t exist')

        call = ContactListEndpoint(
            account.cookies, account.gvoice_key, account.phone_number)
        try:
            contacts = call.get_contact_list()
        except:
            logger.info(
                f'Unable to retrieve contact list from {account.phone_number}.')
            return gvoice_pb2.FetchContactListResponse(success=False, error='unable to process request')

        logger.info(f'Retrieved contact list from {account.phone_number}.')
        return gvoice_pb2.FetchContactListResponse(success=True, recipient_phone_numbers=contacts)

    async def GetGVoiceNumbers(self, request, context):
        gvoice_numbers = self._db.get_all_numbers()

        return gvoice_pb2.FetchGVoiceNumbersResponse(success=True, gvoice_phone_numbers=gvoice_numbers)

    async def GetContactHistory(self, request, context):
        account = self._db.get_account(request.gvoice_phone_number)
        if not account:
            logger.info(
                f'Unable to contact history from {request.gvoice_phone_number} as number registered with GVMS.')
            return gvoice_pb2.FetchContactHistoryResponse(success=False, error='gvoice number doesn\'t exist')

        call = ContactHistoryEndpoint(
            account.cookies, account.gvoice_key, account.phone_number)
        try:
            message_history = call.get_contact_msg_history(
                request.recipient_phone_number, request.num_messages)
        except:
            logger.info(
                f'Unable to retrieve contact history from {account.phone_number}.')
            return gvoice_pb2.FetchContactHistoryResponse(success=False, error='unable to process request')
        message_history = [gvoice_pb2.MessageNode(
            timestamp=message[0], message_contents=message[1], source=message[2]) for message in message_history]

        logger.info(f'Retrieved contact history from {account.phone_number}.')
        return gvoice_pb2.FetchContactHistoryResponse(success=True, messages=message_history)
