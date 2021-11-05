import requests
import logging

from fastapi import Header, HTTPException, Depends
from http import HTTPStatus

from environs import Env

env = Env()
logger = logging.getLogger(__name__)


class OAuthFilter:

    def __init__(self):
        auth_token_url = env.url('auth.token.url')
        self.token_validation_url = auth_token_url.replace('/token', '/user')

    def validate_token(self, token: str):
        headers = dict(Authorization=token)
        try:
            response = requests.get(self.token_validation_url, headers=headers)
            if response.status_code == HTTPStatus.OK:
                return True
        except Exception as exception:
            logger.error(f'Unable to validate the token {str(exception)}')

        return False


def resolve_token(authorization):
    if type(authorization) == str and authorization.startswith('Bearer '):
        return authorization
    return None


def secure(authorization: str = Header(None), oauth_filter: OAuthFilter = Depends(OAuthFilter)):
    token = resolve_token(authorization)
    if not oauth_filter.validate_token(token):
        raise HTTPException(status_code=403, detail='Access Forbidden')
