from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional
from bson import Decimal128
from pydantic import AfterValidator, Field
from store.schemas.base import BaseSchemaMixin, OutMixin


class BaseProduct(BaseSchemaMixin):
    name: str = Field(..., description='Nome do produto')
    quantity: int = Field(..., description='Quantidade do produto')
    price: Decimal = Field(..., description='Preço do produto')
    status: bool = Field(..., description='Disponibilidade do produto')

class ProductIn(BaseProduct):
    ...

class ProductOut(ProductIn, OutMixin):
    ...

def convert_decimal_128(val) -> Decimal128: return Decimal128(str(val))
Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]
class ProductUp(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description='Quantidade do produto')
    price: Optional[Decimal_] = Field(None, description='Preço do produto')
    status: Optional[bool] = Field(None, description='Disponibilidade do produto')
    updated_at: Optional[datetime] = Field(None, description='Data em que o produto foi atualizado')

class ProductUpOut(ProductOut):
    ...
