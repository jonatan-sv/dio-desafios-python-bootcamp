import pytest
from typing import List
from tests.factories import product_data
from fastapi import status


async def test_controller_create_should_return_sucess(client, products_url):
    response = await client.post(products_url, json=product_data())
    content = response.json()
    
    del content['id']
    del content['created_at']
    del content['updated_at']
    
    assert response.status_code == status.HTTP_201_CREATED
    assert content == {'name': 'Produto', 'quantity': 10, 'price': '8500', 'status': True}


async def test_controller_get_should_return_sucess(client, products_url, product_inserted):
    response = await client.get(f'{products_url}{product_inserted.id}')
    content = response.json()

    del content['created_at']
    del content['updated_at']
    
    assert response.status_code == status.HTTP_200_OK
    assert content == {'id': str(product_inserted.id),'name': 'Produto', 'quantity': 10, 'price': '8500', 'status': True}


async def test_controller_get_should_return_not_found(client, products_url):
    response = await client.get(f'{products_url}3cdafcc5-51b7-0000-a19e-763aa783509f')
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == "Product not found with filter: 3cdafcc5-51b7-0000-a19e-763aa783509f" 


@pytest.mark.usefixtures('products_inserted')
async def test_controller_query_should_return_sucess(client, products_url):
    response = await client.get(products_url)
    
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


async def test_controller_patch_should_return_sucess(client, products_url, product_inserted):
    response = await client.patch(f'{products_url}{product_inserted.id}', json={'quantity': '200'})

    assert response.status_code == status.HTTP_200_OK


async def test_controller_patch_should_return_not_found(client, products_url):
    response = await client.patch(f'{products_url}3cdafcc5-51b7-0000-a19e-763aa783509f', json={'quantity': '200'})
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == "Product not found with filter: 3cdafcc5-51b7-0000-a19e-763aa783509f" 


async def test_controller_delete_should_return_no_content(client, products_url, product_inserted):
    response = await client.delete(f'{products_url}{product_inserted.id}')
    
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_return_not_found(client, products_url):
    response = await client.delete(f'{products_url}3cdafcc5-51b7-0000-a19e-763aa783509f')
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == "Product not found with filter: 3cdafcc5-51b7-0000-a19e-763aa783509f" 


@pytest.mark.usefixtures('products_inserted')
async def test_controller_get_by_price_range_should_return_sucess(client, products_url):
    response = await client.get(f'{products_url}price-range?min_price=0&max_price=500')
    
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) == 3


@pytest.mark.usefixtures('products_inserted')
async def test_controller_get_by_price_range_should_return_not_found(client, products_url):
    response = await client.get(f'{products_url}price-range?min_price=10000&max_price=50000')
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == "Product not found with filter: {'price': {'$gte': Decimal128('10000'), '$lte': Decimal128('50000')}}"
