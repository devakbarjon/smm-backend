from fastapi import APIRouter

from .users import router as users_router
from .orders import router as orders_router
from .services import router as services_router
from  .platform import  router as platform_router
from  .categories import router as category_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(orders_router, prefix="/orders", tags=["orders"])
router.include_router(services_router, prefix="/services", tags=["services"])
router.include_router(platform_router, prefix="/platforms", tags=["platforms"])
router.include_router(category_router, prefix="/categories", tags=["categories"])