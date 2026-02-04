from fastapi import APIRouter

from .users import router as users_router
from .orders import router as orders_router
from .services import router as services_router
from  .platforms import  router as platform_router
from  .categories import router as category_router
from .deposit import router as deposit_router
from .transactions import router as transactions_router
from .webhooks import router as webhooks_router
from .admin import router as admin_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(orders_router, prefix="/orders", tags=["orders"])
router.include_router(services_router, prefix="/services", tags=["services"])
router.include_router(platform_router, prefix="/platforms", tags=["platforms"])
router.include_router(category_router, prefix="/categories", tags=["categories"])
router.include_router(deposit_router, prefix="/deposit", tags=["deposit"])
router.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
router.include_router(webhooks_router, prefix="/webhook", tags=["webhook"])

# Admin routes
router.include_router(admin_router, prefix="/admin", tags=["admin"])