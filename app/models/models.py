from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Integer, Numeric, CheckConstraint
from decimal import Decimal
from database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    preco: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    estoque: Mapped[int] = mapped_column(Integer, default=0, nullable=0)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)