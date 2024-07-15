from typing import Annotated
from pydantic import UUID4, Field
from workoutapi.contrib.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Rua X, 002', max_length=60)]
    propietario: Annotated[str, Field(description='Propietário do centro de treinamento', example='Carlos', max_length=20)]


class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=20)]


class CentroTreinamentoOut(CentroTreinamento):
    id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')]