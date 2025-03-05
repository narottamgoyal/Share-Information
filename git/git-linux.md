## Install Git

    sudo apt update
    sudo apt install git

## Check your global Git configuration

    git config --global --list

## Enable Git credential caching by running

    git config --global credential.helper cache

Git will cache these credentials in memory for a short period of time (by default, 15 minutes). You can increase the cache duration if needed. For example, to cache the credentials for 1 hour:

    git config --global credential.helper 'cache --timeout=3600'

## Store Credentials Permanently Using Git's Credential Store

    git config --global credential.helper store

## Unset the credential.helper configuration
If you no longer want to store credentials, you can remove the credential helper by running

    git config --global --unset credential.helper

## Clone the Repository

    git clone https://github.com/username/repository-name.git
