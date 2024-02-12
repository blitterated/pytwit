# syntax=docker/dockerfile:1

FROM pyenv-dde

MAINTAINER blitterated blitterated@protonmail.com

ARG PYTHON_VERSION=3

RUN <<EOT bash -xev
  apt update && apt --yes upgrade
#  apt --yes install build-essential
EOT

# Install a Python and upgrade pip
RUN <<EOT bash -xe
  source /root/.dde.rc/003-pyenv-activation.sh
  pip install -U pip
  pip install python-twitter
EOT

WORKDIR /src

ENTRYPOINT ["/bin/bash"]
