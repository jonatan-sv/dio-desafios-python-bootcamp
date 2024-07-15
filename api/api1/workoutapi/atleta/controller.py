from datetime import datetime
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Body, Query, status
from fastapi_pagination import LimitOffsetPage, paginate
from pydantic import UUID4
from sqlalchemy.future import select
from workoutapi.atleta.models import AtletaModel
from workoutapi.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workoutapi.categorias.models import CategoriaModel
from workoutapi.centro_treinamento.models import CentroTreinamentoModel
from workoutapi.contrib.dependencies import DataBaseDependecy
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


router = APIRouter()


@router.post('/', summary='Cria um novo atleta', status_code=status.HTTP_201_CREATED, response_model=AtletaOut)
async def post(db_session: DataBaseDependecy, AtletaIn: AtletaIn = Body(...)) -> AtletaOut:
    categoria_nome = AtletaIn.categoria.nome
    centro_treinamento_nome = AtletaIn.centro_treinamento.nome
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_nome))).scalars().first()
    
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'A categoria {categoria_nome} não existe')
    
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'O centro de treinamento {centro_treinamento_nome} não existe')
    
    try:
        AtletaOut = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **AtletaIn.model_dump())
        atleta_model = AtletaModel(**AtletaOut.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um atleta cadastrado com o cpf: {atleta_model.cpf}'
        )
    # Erro genérico
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao inserir os dados no banco'
        )
    
    return AtletaOut


@router.get('/', summary='Consulta todos os atletas', status_code=status.HTTP_200_OK, response_model=list[AtletaOut])
async def query(db_session: DataBaseDependecy) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()

    return [AtletaOut.model_validate(atleta) for atleta in atletas]


@router.get('/search', summary='Busca atletas por nome ou CPF', status_code=status.HTTP_200_OK, response_model=LimitOffsetPage[AtletaOut])
async def query(
    db_session: DataBaseDependecy,
    nome: Optional[str] = Query(None, description="Nome a ser pesquisado"),
    cpf: Optional[str] = Query(None, description="CPF a ser pesquisado"),
) -> LimitOffsetPage[AtletaOut]:
    query = select(AtletaModel)
    
    if nome:
        query = query.filter(AtletaModel.nome == nome)
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)
    
    result = await db_session.execute(query)
    atletas= result.scalars().all()
    
    if not atletas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhum atleta foi encontrado.')
        
    return paginate([AtletaOut.model_validate(atleta) for atleta in atletas])


@router.get('/{id}', summary='Consulta um atleta pelo ID', status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def query(id: UUID4, db_session: DataBaseDependecy) -> AtletaOut:
    atletas: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atletas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id {id}')
    return atletas


@router.patch('/{id}', summary='Edita um atleta pelo ID', status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def query(id: UUID4, db_session: DataBaseDependecy, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id {id}')
    # Modify fields
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, val in atleta_update.items():
        setattr(atleta, key, val)
    # Commit and refresh table
    await db_session.commit()
    await db_session.refresh(atleta)
    
    return atleta


@router.delete('/{id}', summary='Apaga um atleta pelo ID', status_code=status.HTTP_204_NO_CONTENT)
async def query(id: UUID4, db_session: DataBaseDependecy) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    # If not found
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id {id}')
    # Delete and commit data
    await db_session.delete(atleta)
    await db_session.commit()