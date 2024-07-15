from fastapi import APIRouter
from store.controllers.product import router as product

api_router = APIRouter()                                                   # Cria um Roteador
api_router.include_router(product, prefix='/products', tags=['products/']) # Adiciona a rota dos produtos