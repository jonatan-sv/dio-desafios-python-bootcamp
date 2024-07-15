import pymongo
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID
from bson import Decimal128
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from store.core.exceptions import InsertErrorException, NotFoundException
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUp, ProductUpOut


class ProductUseCase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")


    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        try:
            await self.collection.insert_one(product_model.model_dump())
        except:
            raise InsertErrorException(message=f'Error inserting data into the database')
        return ProductOut(**product_model.model_dump())


    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})
        if not result:
            raise NotFoundException(message=f'Product not found with filter: {id}')
        return ProductOut(**result)


    async def query(self) -> List[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]


    async def update(self, id: UUID, body: ProductUp) -> ProductUpOut:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f'Product not found with filter: {id}')
        
        new_body = body.model_dump(exclude_none=True)
        # Se o datetime não foi especificado, preencher automáticamente
        if 'updated_at' not in new_body:
            new_body['updated_at'] = datetime.utcnow()

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": new_body},
            return_document=pymongo.ReturnDocument.AFTER
        )
        return ProductUpOut(**result)


    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f'Product not found with filter: {id}')

        result = await self.collection.delete_one(filter={"id": id})
        return True if result.deleted_count > 0 else False
    
    
    async def get_products_by_price_range(self, min_price: Decimal, max_price: Decimal) -> List[ProductOut]:
        min = Decimal128(str(min_price))
        max = Decimal128(str(max_price))

        query = {"price": {"$gte": min, "$lte": max}}
        products = [ProductOut(**item) async for item in self.collection.find(query)]
        if not products:
            raise NotFoundException(message=f'Product not found with filter: {query}')
        return products



product_usecase = ProductUseCase()
