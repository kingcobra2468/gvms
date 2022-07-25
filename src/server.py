import asyncio
import logging
import sys

import grpc

from config import HOST_PORT, HOST_ADDRESS, MTLS_ENABLED, SECRETS_DIR, \
    SERVER_CERT_PATH, SERVER_KEY_PATH, CLIENT_CERT_PATH
from db.account_store import AccountStore
from api.v1.gvoice_handler import GVoiceHandler
import api.v1.gvoice_pb2
import api.v1.gvoice_pb2_grpc


logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


async def serve() -> None:
    listen_addr = f'{HOST_ADDRESS}:{HOST_PORT}'
    server = grpc.aio.server()

    api.v1.gvoice_pb2_grpc.add_GVoiceServicer_to_server(
        GVoiceHandler(), server)

    if MTLS_ENABLED:
        server_credentials = grpc.ssl_server_credentials(
            [[open(SERVER_KEY_PATH, 'rb').read(), open(SERVER_CERT_PATH, 'rb').read()],
             ],
            root_certificates=open(CLIENT_CERT_PATH, 'rb').read(),
            require_client_auth=True
        )
        server.add_secure_port(listen_addr, server_credentials)
    else:
        server.add_insecure_port(listen_addr)

    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    db = AccountStore.get_instance(SECRETS_DIR)
    db.load_accounts()

    asyncio.run(serve())
    logging.info(f'Serving on port {HOST_PORT}.')
