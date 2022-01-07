import os

from dotenv import load_dotenv

load_dotenv()


HOST_ADDRESS = os.environ.get('HOST_ADDRESS', 'localhost')
HOST_PORT = os.environ.get('HOST_PORT', 50051)

SECRETS_DIR = os.environ.get('SECRETS_DIR', None)
if not SECRETS_DIR:
    raise ValueError(
        'SECRETS_DIR environment variable not found.')
MTLS_ENABLED = int(os.environ.get('MTLS_ENABLED', 0))

SERVER_KEY_PATH = os.environ.get('SERVER_KEY_PATH', None)

if not SERVER_KEY_PATH and MTLS_ENABLED:
    raise ValueError(
        'SERVER_KEY_PATH environment variable not found.')

SERVER_CERT_PATH = os.environ.get('SERVER_CERT_PATH', None)
if not SERVER_CERT_PATH and MTLS_ENABLED:
    raise ValueError(
        'SERVER_CERT_PATH environment variable not found.')

CLIENT_CERT_PATH = os.environ.get('CLIENT_CERT_PATH', None)
if not CLIENT_CERT_PATH and MTLS_ENABLED:
    raise ValueError(
        'CLIENT_CERT_PATH environment variable not found.')
