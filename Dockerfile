FROM python:3.7

ARG host_address=0.0.0.0
ARG host_port
ARG secrets_dir=/gvms/secrets
ARG mtls_enabled=0
ARG server_key_path
ARG server_cert_path
ARG client_cert_path

ENV HOST_ADDRESS=${host_address}
ENV HOST_PORT=${host_port}
ENV SECRETS_DIR=${secrets_dir}
ENV MTLS_ENABLED=${mtls_enabled}
ENV SERVER_KEY_PATH=${server_key_path}
ENV SERVER_CERT_PATH=${server_cert_path}
ENV CLIENT_CERT_PATH=${client_cert_path}

COPY src/ /opt/gvms/
COPY requirements.txt /tmp

RUN mkdir -p /gvms/secrets /gvms/keys
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /opt/gvms

VOLUME /gvms/secrets
VOLUME /gvms/keys

ENTRYPOINT ["python3", "server.py"]