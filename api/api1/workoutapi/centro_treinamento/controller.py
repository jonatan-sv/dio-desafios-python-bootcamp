from uuid import uuid4
from fastapi import APIRouter, Body, status
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from workoutapi.centro_treinamento.models import CentroTreinamentoModel
from workoutapi.centro_treinamento.schemas import CentroTreinamento, CentroTreinamentoOut
from workoutapi.contrib.dependencies import DataBaseDependecy
from fastapi import HTTPException


router = APIRouter()


@router.post('/', summary='Cria um novo Centro de Treinamento', status_code=status.HTTP_201_CREATED, response_model=CentroTreinamentoOut)
async def post(
    db_session: DataBaseDependecy, 
    centro_treinamento_in: CentroTreinamento = Body(...)
    ) -> CentroTreinamentoOut:
    
    try:
        centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
        centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
        db_session.add(centro_treinamento_model)
        await db_session.commit()
    
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um centro de treinamento com o nome: {centro_treinamento_model.nome}'
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao inserir os dados no banco'
        )
    
    return centro_treinamento_out


@router.get('/', summary='Consulta todos os Centros de Treinamento', status_code=status.HTTP_200_OK, response_model=list[CentroTreinamentoOut])
async def query(db_session: DataBaseDependecy) -> list[CentroTreinamentoOut]:
    centro_treinamento: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return centro_treinamento


@router.get('/{id}', summary='Consulta um Centro de Treinamento pelo ID', status_code=status.HTTP_200_OK, response_model=CentroTreinamentoOut)
async def query(id: UUID4, db_session: DataBaseDependecy) -> CentroTreinamentoOut:
    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Centro de treinamento não encontrado no id {id}')

    return centro_treinamento