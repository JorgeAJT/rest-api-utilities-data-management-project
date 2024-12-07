from fastapi import APIRouter
from .mandate_data import (mandate_data_get_router, mandate_data_post_router,
                           mandate_data_put_router, mandate_data_delete_router)

api_router = APIRouter()
api_router.include_router(mandate_data_get_router)
api_router.include_router(mandate_data_post_router)
api_router.include_router(mandate_data_put_router)
api_router.include_router(mandate_data_delete_router)