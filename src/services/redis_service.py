import logging

from ..configs.redis_datasource import RedisDatasource

logger = logging.getLogger(__name__)


class RedisService:

    def __init__(self, redis_datasource: RedisDatasource):
        self.redis_datasource = redis_datasource

    def get_lock(self, key: str, key_expiry: int):
        redis_response = self.redis_datasource.set_key(key, key_expiry)
        if redis_response:
            logger.info(f'{key} is set in Redis')
            return dict(status=201, message=f'{key} is unique')

        logger.info(f'{key} is duplicate')
        return dict(status=406, message=f'{key} is duplicate')
