from typing import Annotated
from pydantic import UUID4, Field
from workoutapi.contrib.schemas import BaseSchema


class Categoria(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=10)]

class CategoriaOut(Categoria):
    id: Annotated[UUID4, Field(description='Identificador da categoria')]