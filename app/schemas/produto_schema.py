from pydantic import BaseModel, ConfigDict, field_validator, Field
from decimal import Decimal
from app.core.exceptions import BusinessError

class ProdutoCreate(BaseModel):
    nome: str = Field(min_length=1)
    preco: Decimal = Field(ge=0)
    estoque: int = Field(ge=0)

    @field_validator("preco")
    @classmethod
    def validar_preco(cls, preco: Decimal) -> Decimal:
        if preco <= 0:
            raise BusinessError(
                code="PRICE_TOO_LOW",
                message="Preço não pode ser menor que zero",
                details={"preco": str(preco)}
            )
        return preco

    @field_validator("estoque")
    @classmethod
    def validar_estoque(cls, estoque: int) -> int:
        if estoque < 0:
            raise BusinessError(
                code="INVENTORY_TOO_LOW",
                message="Estoque não pode ser menor que zero",
                details={"estoque": estoque}
            )
        return estoque

class ProdutoResponse(ProdutoCreate):
    id: int
    ativo: bool
    model_config = ConfigDict(from_attributes=True) 