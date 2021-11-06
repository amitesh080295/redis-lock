from dependency_injector import containers, providers
from environs import Env

from ..services.redis_service import RedisService
from ..security.authenticator import AuthenticationHandler
from ..configs.config_client import PythonConfigClient
from ..configs.redis_datasource import RedisDatasource


class Container(containers.DeclarativeContainer):
    configs = providers.Configuration()

    env = providers.Singleton(
        Env
    )

    auth_handler = providers.Singleton(
        AuthenticationHandler,
        env=env
    )

    python_config_client = providers.Singleton(
        PythonConfigClient,
        auth_handler=auth_handler,
        env=env
    )

    redis_datasource = providers.Singleton(
        RedisDatasource
    )

    redis_service = providers.Singleton(
        RedisService,
        redis_datasource=redis_datasource
    )
