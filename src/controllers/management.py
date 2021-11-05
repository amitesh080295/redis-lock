from fastapi import APIRouter

management_router = APIRouter(
    prefix='/management'
)


@management_router.get('/health')
def health_check():
    return dict(status='UP')
