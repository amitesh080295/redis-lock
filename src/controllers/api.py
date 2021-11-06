from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from ..configs.containers import Container
from ..services.redis_service import RedisService

import logging
logger = logging.getLogger(__name__)

api_router = APIRouter(
    prefix='/api/v1'
)


@api_router.get('/lock')
@inject
def sample(
        key: str,
        key_expiry: int,
        redis_service: RedisService = Depends(Provide[Container.redis_service])
):
    return redis_service.get_lock(key, key_expiry)
