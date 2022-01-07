# **GVMS**
Google Voice microservice(GVMS) is a gRPC-based microservice for interacting
with Google Voice APIs. Offers a way to send text messages, view contact message
history, and get full contact list from Google Voice.

## **Capabilities**
The existing feature set of GVMS includes:
- ability to send a text message to a given phone-number.
- capability to see full text message history between a given contact.
- ability to see all contact phone number list for a given account.

## **Limitations**
For simplicity, image-only messages when fetching message history and group messages
are currently not supported and are filtered from results.

## **Paging**
As a result of some APIs requiring paging, multiple calls are internally performed
for some of the endpoints (e.g. fetching message history and contact list). Cardinality
of the actual lists is calculated by polling from an exponential sequence of the
function 2^n. This is done until the response cardinality no longer grows which indicates
that all data has been fetched. Nevertheless, this architecture might lead to these RPC
calls taking a few seconds as there is an internal cool down to avoid flagging.

## **Security**
GVMS supports both unsecure and mTLS. Thus, configure GVMS based on your needs by setting
the appropriate config settings. 

## **Config**
By copying `env.template` into `/src` as `.env` (e.g. `cp env.template src/.env`),
the following config options can then be set:
- **HOST_ADDRESS=** the host address of GVMS.
- **HOST_PORT=** the port address of GVMS.
- **SECRETS_DIR=** the directory where GVoice account secret dumps are placed.
- **MTLS_ENABLED=** whether to enable mTLS. Set `1` for true and `0` for false.
- **SERVER_KEY_PATH=** server key path for mTLS. Only set if MTLS_ENABLED is `1`.
- **SERVER_CERT_PATH=** server cert path for mTLS. Only set if MTLS_ENABLED is `1`.
- **CLIENT_CERT_PATH=** client cert path for mTLS. Only set if MTLS_ENABLED is `1`.

## **Setup**
The following setup is required to get GVMS running:
1. Get secret dumps for N number of Google Accounts following and running
   [this](https://github.com/kingcobra2468/GVoiceSecretDump).
2. Install dependencies with `pip3 install -r requirements.txt`.
3. Setup config `.env` with appropriate options.
4. Enter `src/` and run GVMS with `python3 server.py`.