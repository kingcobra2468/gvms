import asyncio
import os

from dotenv import load_dotenv
import grpc

from db.account_store import AccountStore
from api.gvoice_handler import GVoiceHandler
import api.gvoice_pb2
import api.gvoice_pb2_grpc


async def serve() -> None:
    server = grpc.aio.server()
    api.gvoice_pb2_grpc.add_GVoiceServicer_to_server(GVoiceHandler(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    load_dotenv()

    secrets_dir = os.environ.get('SECRETS_DIR', None)
    if not secrets_dir:
        raise ValueError(
            'Make sure .env file exists and includes all env vars')
    db = AccountStore.get_instance(secrets_dir)
    db.load_accounts()

    asyncio.run(serve())
