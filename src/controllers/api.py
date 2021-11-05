from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from ..configs.containers import Container
from ..services.sample_service import SampleService

import logging
logger = logging.getLogger(__name__)

api_router = APIRouter(
    prefix='/api/v1'
)


@api_router.get('/sample_endpoint')
@inject
def sample(
        sample_service: SampleService = Depends(Provide[Container.sample_service])
):
    return sample_service.sample_method()