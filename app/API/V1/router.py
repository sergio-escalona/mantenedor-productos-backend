from fastapi import APIRouter
from. modules.auth.routes import router as auth_router
from .modules.users.routes import router as users_router
from .modules.products.routes import router as products_router
from .modules.product_categories.routes import router as categories_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(products_router)
router.include_router(categories_router)