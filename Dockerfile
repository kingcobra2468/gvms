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

# Install chrome
RUN apt-get update && apt-get install -y
RUN wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.198-1_amd64.deb
RUN dpkg -i google-chrome-stable_114.0.5735.198-1_amd64.deb || true
RUN apt-get -f -y install

# Install chromedriver
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip && ls && mv chromedriver /usr/local/bin

RUN rm -fr chromedriver_linux64.zip google-chrome-stable_114.0.5735.198-1_amd64.deb LICENSE.chromedriver

WORKDIR /opt/gvms

VOLUME /gvms/secrets
VOLUME /gvms/keys

ENTRYPOINT ["python3", "server.py"]