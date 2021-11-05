import json
import base64
import requests
import datetime
import logging

from environs import Env

logger = logging.getLogger(__name__)


class AuthenticationHandler:

    def __init__(self, env: Env):
        auth_username = env.str('oauth.username')
        auth_password = env.str('oauth.password')

        auth_credentials = auth_username + ':' + auth_password
        encoded_auth_credentials = (base64.b64encode(bytes(auth_credentials, 'utf-8'))).decode('utf-8')

        self.auth_token_url = env.url('auth.token.url')
        self.headers = dict(Authorization='Basic ' + encoded_auth_credentials)
        self.token = str()
        self.token_expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=25)

    def get_auth_token(self):
        if datetime.datetime.now() > self.token_expiry_time or self.token == '':
            try:
                response = requests.get(self.auth_token_url, headers=self.headers)
                decoded_response = response.content.decode('UTF-8')

                if decoded_response is not None:
                    jwt_token = json.loads(decoded_response).get('token')
                    self.token = 'Bearer ' + jwt_token
                    self.token_expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=25)
                else:
                    logger.error('No JWT token fetched')

            except Exception as exception:
                logger.error(f'Error in getting auth token {str(exception)}')
                raise

        return self.token
