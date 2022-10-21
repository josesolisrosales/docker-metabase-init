# docker-metabase-init
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/josesolisrosales/docker-metabase-init/release?style=flat-square)
![Docker Pulls](https://img.shields.io/docker/pulls/josesolisrosales/metabase-init?style=flat-square)
![Docker Image Version (latest by date)](https://img.shields.io/docker/v/josesolisrosales/metabase-init?style=flat-square)

Docker image to be used as a sidecar container to initialize a metabase instance.

## Usage
```
usage: scratch.py [-h] [--url URL] [--setup-email SETUP_EMAIL] [--setup-firstname SETUP_FIRSTNAME] [--setup-lastname SETUP_LASTNAME] [--setup-password SETUP_PASSWORD] [--retries RETRIES] [--backoff-in-seconds BACKOFF_IN_SECONDS]

optional arguments:
  -h, --help                                         show this help message and exit
  --url URL, -u            URL                       Metabase URL
  --setup-email            SETUP_EMAIL               Initial user email
  --setup-firstname        SETUP_FIRSTNAME           Initial user first name
  --setup-lastname         SETUP_LASTNAME            Initial user last name
  --setup-password         SETUP_PASSWORD            Initial user password
  --retries                RETRIES                   Number of retries
  --backoff-in-seconds     BACKOFF_IN_SECONDS        Initial backoff time
```