# ubuntuのイメージをプルし、Pythonをインストールしていく
FROM ubuntu:20.04

SHELL ["/bin/bash", "-c"]

# pythonをインストール
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y python3.8 python3.8-dev \
    && source ~/.bashrc \
    && apt-get -y install vim

# 作業ディレクトリを設定
WORKDIR /usr/src/app

# 環境変数を設定
# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE 1
# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

# 依存関係のインストールとpipenvをインストール
RUN apt-get install -y curl \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && apt-get install -y python3.8-distutils \
    && python3.8 get-pip.py \
    && pip install -U pip \
    && apt-get install -y build-essential libssl-dev libffi-dev python-dev python3-dev libpq-dev

# パスワード登録時のハッシュ化のためargon2をインストール
RUN python3 -m pip install argon2_cffi \
    && python3 -m pip install -U cffi pip setuptools

# pipenvのインストール
RUN pip install pipenv

# ローカルマシンののPipfileをコンテナにコピー
COPY Pipfile ./

# Pipfile.lockを無視してPipfileに記載のパッケージをシステムにインストール
# その後、pipenvをアンインストール
RUN pipenv install --system --skip-lock \
    && pip uninstall -y pipenv virtualenv-clone virtualenv

# Ubuntuパッケージ最新化
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y python3.8

RUN apt-get install -y netcat \
    && apt-get install -y expect

# シェルスクリプトをコピー
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app/

# シェルスクリプトを実行
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]