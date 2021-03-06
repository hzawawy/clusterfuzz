# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
FROM ubuntu:16.04

RUN mkdir /data
WORKDIR /data

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    apt-get install -y \
        apt-transport-https \
        build-essential \
        curl \
        gdb \
        libbz2-dev \
        libcurl4-openssl-dev \
        libffi-dev \
        libgdbm-dev \
        liblzma-dev \
        libncurses5-dev \
        libnss3-dev \
        libreadline-dev \
        libssl-dev \
        locales \
        lsb-release \
        net-tools \
        python \
        python-dbg \
        python-dev \
        python-pip \
        socat \
        sudo \
        unzip \
        util-linux \
        wget \
        zip \
        zlib1g-dev

# Install patchelf.
RUN curl -sS https://releases.nixos.org/patchelf/patchelf-0.9/patchelf-0.9.tar.bz2 | tar -C /tmp -xj && \
    cd /tmp/patchelf-*/ && \
    ./configure --prefix=/usr && \
    make install

# Install Python 3.
RUN curl -sS https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz | tar -C /tmp -xzv && \
    cd /tmp/Python-3.7.7 && \
    ./configure --enable-optimizations && make altinstall && \
    rm -rf /tmp/Python-3.7.7
RUN pip3.7 install pipenv

# Install Google Cloud SDK.
RUN CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -  && \
    apt-get update && apt-get install -y google-cloud-sdk

# Only upgrade python packages used by fuzzers and infrastructure.
RUN pip2 install --upgrade pip
COPY requirements.txt .
RUN pip2 install -r requirements.txt

# Set up google-fluentd
# We ignore errors in install-logging-agent.sh as it always fails to start
# after installation without a metadata server.
RUN curl -sSO https://dl.google.com/cloudagents/install-logging-agent.sh && \
    bash install-logging-agent.sh || true && \
    sed -i 's/flush_interval 5s/flush_interval 60s/' /etc/google-fluentd/google-fluentd.conf
COPY clusterfuzz-fluentd.conf /etc/google-fluentd/config.d/clusterfuzz.conf

# Common environment variables.
ENV USER=clusterfuzz
ENV INSTALL_DIRECTORY /mnt/scratch0
ENV BOT_TMPDIR $INSTALL_DIRECTORY/tmp
ENV ROOT_DIR $INSTALL_DIRECTORY/clusterfuzz
ENV UPDATE_WEB_TESTS True
ENV PYTHONPATH $INSTALL_DIRECTORY/clusterfuzz/src
ENV RUN_CMD "python3.7 $ROOT_DIR/src/python/bot/startup/run.py"
ENV DEPLOYMENT_ZIP "linux-3.zip"

# Passwordless sudo (needed for AFL launcher).
RUN groupadd nopwsudo && \
    echo "%nopwsudo ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/mysudoers

# Make sure GSUtil uses the GCE service account.
RUN echo '[GoogleCompute]\nservice_account = default' > /etc/boto.cfg

VOLUME $INSTALL_DIRECTORY
WORKDIR $INSTALL_DIRECTORY

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV PYTHONIOENCODING UTF-8

COPY setup_common.sh setup_clusterfuzz.sh setup_nfs.sh start_clusterfuzz.sh setup_mock_metadata.sh start.sh Pipfile Pipfile.lock /data/
RUN cd /data && \
    # Make pip3.7 the default so that pipenv install --system works.
    mv /usr/local/bin/pip3.7 /usr/local/bin/pip && \
    pipenv install --deploy --system
CMD ["bash", "-ex", "/data/start.sh"]

