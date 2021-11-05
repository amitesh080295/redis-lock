from fastapi import FastAPI

from .configs.containers import Container
from .controllers import api, management

import logging

logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[api])

    application = FastAPI()
    application.container = container

    application.include_router(api.api_router)
    application.include_router(management.management_router)

    return application


app = create_app()
