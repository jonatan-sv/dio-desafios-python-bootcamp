import asyncio
from typing import List
import uuid
import pytest
from store.db.mongo import db_client
from store.schemas.product import ProductIn, ProductUp
from tests.factories import product_data, products_data
from store.usecases.product import product_usecase
from httpx import AsyncClient


# Cria um event loop para testes async
@pytest.fixture(scope="session")
def event_loop():
    loop =  asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Cria um cliente Mongo para os testes
@pytest.fixture
def mongo_client():
    return db_client.get()

# Limpa as coleções após finalizar os testes
@pytest.fixture(autouse=True)
async def clear_collections(mongo_client):
    yield
    collections_names = await mongo_client.get_database().list_collection_names()
    for collection_name in collections_names:
        if collection_name.startswith("system"):
            continue
        await mongo_client.get_database()[collection_name].delete_many({})

# Cria um client HTTPS
@pytest.fixture
async def client():
    from store.main import app
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac

# URL do endpoint dos produtos
@pytest.fixture
def products_url() -> str:
    return '/products/'

# Gera um  único produto
@pytest.fixture
def product_in() -> ProductIn:
    return ProductIn(**product_data(), id=uuid.UUID("3cdafcc5-51b7-49f9-a19e-763aa783509f"))

# Insere um únicop produto no DB
@pytest.fixture
async def product_inserted(product_in) -> ProductIn:
    return await product_usecase.create(body=product_in)

# Gera uma atualização de produto
@pytest.fixture
def product_up() -> ProductUp: 
    return ProductUp(**product_data(), id=uuid.UUID("3cdafcc5-51b7-49f9-a19e-763aa783509f"))

# Gera múltiplos produtos
@pytest.fixture
def products_in() -> List[ProductIn]:
    return [ProductIn(**product, id=uuid.UUID("3cdafcc5-51b7-49f9-a19e-763aa783509f")) for product in products_data()]

# Insere múltiplos produtos no DB
@pytest.fixture
async def products_inserted(products_in) -> List[ProductIn]:
    return [await product_usecase.create(body=product_in) for product_in in products_in]