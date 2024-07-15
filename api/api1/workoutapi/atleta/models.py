from datetime import datetime
from workoutapi.contrib.models import BaseModel
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AtletaModel(BaseModel):
    __tablename__ = 'atletas'
    # Primary Key ID
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    categoria: Mapped['CategoriaModel'] = relationship(back_populates='atleta', lazy='selectin')
    categoria_id: Mapped[int] = mapped_column(ForeignKey('categorias.pk_id'))
    centro_treinamento: Mapped['CentroTreinamentoModel'] = relationship(back_populates='atleta', lazy='selectin')
    centro_treinamento_id: Mapped[int] = mapped_column(ForeignKey('centro_treinamento.pk_id'))