import uuid
import pytest
from typing import List
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductOut, ProductUpOut
from store.usecases.product import product_usecase


async def test_usecases_create_should_return_sucess(product_in):
    result = await product_usecase.create(body=product_in)
    
    assert isinstance(result, ProductOut)
    assert result.name == 'Produto'


async def test_usecases_get_should_return_sucess(product_inserted):
    result = await product_usecase.get(product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == 'Produto'
    

async def test_usecases_get_should_return_not_found():
    with pytest.raises(NotFoundException) as e:
        await product_usecase.get(id=uuid.UUID("3cdafcc5-51b7-0000-a19e-763aa783509f"))

    assert e.value.message == 'Product not found with filter: 3cdafcc5-51b7-0000-a19e-763aa783509f'
    

@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_sucess():
    result = await product_usecase.query()
    
    assert isinstance(result, List)
    assert len(result) > 1


async def test_usecases_update_should_return_sucess(product_up, product_inserted):
    product_up.price = '7500'
    result = await product_usecase.update(id=product_inserted.id, body=product_up)
    
    assert isinstance(result, ProductUpOut)


async def test_usecases_delete_should_return_sucess(product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)
    
    assert result is True
    

async def test_usecases_delete_should_return_not_found():
    with pytest.raises(NotFoundException) as e:
        await product_usecase.delete(id=uuid.UUID("3cdafcc5-51b7-0000-a19e-763aa783509f"))
    
    assert e.value.message == 'Product not found with filter: 3cdafcc5-51b7-0000-a19e-763aa783509f'