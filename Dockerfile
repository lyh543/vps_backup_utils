FROM python:3.7-buster
WORKDIR /code
RUN pip3 install poetry
# Comment the following line if you don't need debian mirrors in China
RUN wget -O /etc/apt/sources.list https://mirrors.cloud.tencent.com/repo/debian10_sources.list
RUN apt update && \
    apt install -y ssh rsync tar gzip default-mysql-client postgresql-client-common
COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY . ./
CMD ["poetry", "run", "pytest"]