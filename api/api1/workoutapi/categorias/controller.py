from uuid import uuid4
from fastapi import APIRouter, Body, status
from pydantic import UUID4
from sqlalchemy.future import select
from workoutapi.categorias.models import CategoriaModel
from workoutapi.categorias.schemas import Categoria, CategoriaOut
from workoutapi.contrib.dependencies import DataBaseDependecy
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


router = APIRouter()


@router.post('/', summary='Cria uma nova categoria', status_code=status.HTTP_201_CREATED, response_model=CategoriaOut)
async def post(
    db_session: DataBaseDependecy, 
    categoria_in: Categoria = Body(...)
    ) -> CategoriaOut:
    
    try:
        categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
        categoria_model = CategoriaModel(**categoria_out.model_dump())
        db_session.add(categoria_model)
        await db_session.commit()

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe uma categoria com o nome: {categoria_model.nome}'
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao inserir os dados no banco'
        )

    return categoria_out


@router.get('/', summary='Consulta todas as categorias', status_code=status.HTTP_200_OK, response_model=list[CategoriaOut])
async def query(db_session: DataBaseDependecy) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return categorias


@router.get('/{id}', summary='Consulta uma categoria pelo ID', status_code=status.HTTP_200_OK, response_model=CategoriaOut)
async def query(id: UUID4, db_session: DataBaseDependecy) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Categoria não encontrada no id {id}')
    return categoria