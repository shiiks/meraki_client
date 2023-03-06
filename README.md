# Meraki API Client
This repository contains a Python client for the Meraki API, which can be used to fetch lists of organizations, networks within an organization, and devices within a network. The client also includes a TTL caching mechanism to store the data fetched in the first execution to speed up future executions.

# Getting Started
Before using the Meraki API client, you will need to obtain an API key from the Meraki Dashboard. Once you have your API key, you can either set it as an environment variable or pass it as a parameter when initializing the client.

To install the necessary dependencies, you can use pip:
```
pip install -r requirements.txt
```

# Usage
```
export API_URL=<MERAKI_API_URL>
EXPORT MERAKI_X_AUTH_TOKEN=<MERAKI_X_AUTH_TOKEN>
python get_meraki.py
```

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/Shikhar447/meraki_client)
[![Run in Cisco Cloud IDE](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-runable-icon.svg)](https://developer.cisco.com/devenv/?id=devenv-vscode-base&GITHUB_SOURCE_REPO=https://github.com/Shikhar447/meraki_client)
