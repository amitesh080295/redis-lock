import json
import requests
import re
import logging

from ..security.authenticator import AuthenticationHandler
from environs import Env

logger = logging.getLogger(__name__)


def parse_config(property_sources):
    config_server_properties = {}
    property_sources.reverse()

    for property_source in property_sources:
        config_server_properties.update(property_source['source'])

    return config_server_properties


class PythonConfigClient:

    def __init__(self, auth_handler: AuthenticationHandler, env: Env):
        self.address = env.str('config-address')
        self.branch = env.str('branch')
        self.profile = env.str('profile')
        self.app_name = env.str('app-name')
        self.profile = self.profile.replace(',', '%2C')
        config_url = self.address + '/' + self.app_name + '/' + self.profile + '/' + self.branch
        headers = {'X-Config-Token': auth_handler.get_auth_token()}

        try:
            logger.info('Getting the properties from the config server')
            response = requests.get(config_url, headers=headers)
            decoded_response = response.content.decode('utf-8')
            property_sources = json.loads(decoded_response)['propertySources']
            self.CONFIG_SERVER_PROPERTIES = parse_config(property_sources)
            logger.info('Config properties have been successfully fetched')
        except Exception as exception:
            logger.error('Failed to fetch configs from config server' + str(exception))

    def serve_value(self, key):
        value = str(self.CONFIG_SERVER_PROPERTIES.get(key))
        match = re.search('(?<=\${)[a-zA-Z0-9.-]*(?=})', value)
        if match:
            sub_key = match.group(0)
            return value.replace('${' + sub_key + '}', str(self.CONFIG_SERVER_PROPERTIES.get(sub_key)))
        else:
            return value
