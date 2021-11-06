import redis
import logging

logger = logging.getLogger(__name__)


class RedisDatasource:

    def __init__(self):
        logger.info('Connecting to Redis...')

        try:
            self.redis_connection = redis.Redis(
                host='localhost',
                port=6379,
                db=0
            )
            logger.info('Successfully connected to Redis')
        except Exception as exception:
            logger.error(f'Unable to connect to Redis ${str(exception)}')
            raise

    def set_key(self, key: str, key_expiry: int):
        return self.redis_connection.set(key, 'DUMMY', ex=key_expiry, nx=True)
