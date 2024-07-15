from decimal import Decimal
from typing import List
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from store.core.exceptions import InsertErrorException, NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUp, ProductUpOut
from store.usecases.product import ProductUseCase

router = APIRouter()


@router.post('/', summary='Cria um produto', status_code=status.HTTP_201_CREATED, response_model=ProductOut)
async def post(body: ProductIn = Body(...), usecase: ProductUseCase = Depends()) -> ProductOut:
    try:
        return await usecase.create(body=body)
    except InsertErrorException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message)


@router.get('/price-range', summary='Busca produtos por intervalo de preço', status_code=status.HTTP_200_OK, response_model=List[ProductOut])
async def get_products_by_price_range(
    min_price: Decimal = Query(..., description="Preço mínimo"),
    max_price: Decimal = Query(..., description="Preço máximo"),
    usecase: ProductUseCase = Depends()
) -> List[ProductOut]:
    try:
        return await usecase.get_products_by_price_range(min_price=min_price, max_price=max_price)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.get('/{id}', summary='Busca um produto pelo ID', status_code=status.HTTP_200_OK, response_model=ProductOut)
async def get_product(id: UUID = Path(..., alias='id'), usecase: ProductUseCase = Depends()) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.get('/', summary='Mostra todos os produtos', status_code=status.HTTP_200_OK, response_model=List[ProductOut])
async def get_all_products(usecase: ProductUseCase = Depends()) -> List[ProductOut]:
    return await usecase.query()


@router.patch('/{id}', summary='Atualiza um produto', status_code=status.HTTP_200_OK, response_model=ProductUpOut)
async def patch_product(id: UUID = Path(..., alias='id'), body: ProductUp = Body(...), usecase: ProductUseCase = Depends()) -> ProductUpOut:
    try:
        return await usecase.update(id=id, body=body)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.delete('/{id}', summary='Apaga um produto', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: UUID = Path(..., alias='id'), usecase: ProductUseCase = Depends()) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
