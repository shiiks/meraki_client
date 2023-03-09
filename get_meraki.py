#!/usr/bin/env python

"""Author: Shikhar Saran Srivastava 
Purpose: This script uses Meraki API to fetch list of organisations, networks and
devices, it leverages Cisco DevNet sandboxes. 
"""

import requests
import logging
import json
import os
from dotenv import load_dotenv
from cachetools import cached, TTLCache

load_dotenv()
logging.basicConfig(filename='app.log', level=logging.DEBUG, filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


class Meraki:

    def __init__(self):
        self.api_url = os.getenv('API_URL')
        self.api_token = os.getenv('MERAKI_X_AUTH_TOKEN')
        self.headers = {
            "Accept": "application/json",
            "X-Cisco-Meraki-API-Key": self.api_token
        }

    @staticmethod
    def http_get_requests(url, headers, auth_username=None, auth_password=None):
        """
        This function request the API URL for making GET request to Meraki API.
        :param: url: The API endpoint from which the GET request will be sent.
        :param: headers: Headers needed for making the HTTP GET request.
        :param: auth_username: Username for basic authentication if required else None will be used.
        :param: auth_password: Password for basic authentication if required else None will be used.
        :return: API response data as results if found else returns ERROR message with a reason.
        """
        try:
            if auth_username is None:
                response_from_api = requests.get(url=url, headers=headers)
            else:
                response_from_api = requests.get(url=url, headers=headers, auth=(auth_username, auth_password))

            if response_from_api.status_code != 200:
                return response_from_api.json()
            response_json = response_from_api.json()
        except requests.ConnectionError as exception:
            response_json = {
                "ERROR": f"Unable to connect to {url} because {exception}"
            }
        except requests.HTTPError as exception:
            response_json = {
                "ERROR": f"HTTP error occured while communicating to {url} because {exception}"
            }
        except json.decoder.JSONDecodeError as exception:
            response_json = {
                "ERROR": f"JSONDecodeError occured while communicating to {url} because {exception}"
            }
        return response_json

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_devices_in_organisations(self):
        """
        This fucntion fetches list of organisations, networks inside the organisation and devices inside the network.
        :return: Returns the list of devices if found else returns an empty list of JSON object.
        """
        devices = {}
        try:
            organisations = self.http_get_requests(f"{self.api_url}/organizations", self.headers)
            for organisation in organisations:
                if 'devnet' in organisation['name'].lower():
                    organisation_id = organisation['id']
                    logging.info(f"Organisation ID: {organisation_id}")
                    networks = self.http_get_requests(f"{self.api_url}/organizations/{organisation_id}/networks",
                                                      self.headers)
                    for network in networks:
                        if 'id' in network:
                            network_id = network['id']
                            logging.info(f"Network IDs found in {organisation_id} are: {network_id}")
                            devices = self.http_get_requests(
                                f"{self.api_url}/organizations/{organisation_id}/networks/{network_id}/devices",
                                self.headers)
                            logging.info(f"Device found in {organisation_id} and Network ID {network_id} are: {devices}")
                        else:
                            continue
        except Exception as exception:
            logging.info(f"Error: {exception}")
        return devices


if __name__ == "__main__":
    meraki = Meraki()
    meraki.get_devices_in_organisations()
