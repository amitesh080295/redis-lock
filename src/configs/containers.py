from dependency_injector import containers, providers
from environs import Env

from ..services.sample_service import SampleService
from ..security.authenticator import AuthenticationHandler
from ..configs.config_client import PythonConfigClient


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

    sample_service = providers.Singleton(
        SampleService
    )
