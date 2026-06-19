from app.repository.produto_repository import *
from app.schemas.produto_schema import ProdutoCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import BusinessError, NotFoundError

def criar_produto_service(db: Session, produto: ProdutoCreate):
    if buscar_produto_por_nome_repository(db, produto.nome):
        raise BusinessError(
            code="PRODUCT_ALREADY_EXISTS",
            message="Produto com esse nome já existe",
            details={"nome_produto": produto.nome}
        )
    try:
        novo_produto = criar_produto_repository(db, produto)
        db.commit()
        db.refresh(novo_produto)
        return novo_produto
    except SQLAlchemyError:
        db.rollback()
        raise BusinessError(
            code="PRODUCT_CREATION_FAILED",
            message="Não foi possível criar o produto.",
            status_code=500,
        )
    
def buscar_produto_por_id_service(db: Session, id: int):
    produto = buscar_produto_por_id_repository(db, id)
    if not produto:
        raise NotFoundError(
            code="PRODUCT_NOT_FOUND",
            message="Produto não encontrado",
            details={"produto_id": id},
            
        )
    return produto

def buscar_produto_por_nome_service(db: Session, nome: str):
    produto = buscar_produto_por_nome_repository(db, nome)
    if not produto:
        raise NotFoundError(
            code="PRODUCT_NOT_FOUND",
            message="Produto não encontrado",
            details={"produto_id": id}
        )
    return produto

def listar_produtos_service(db: Session, limit: int, offset: int):
    return listar_produtos_repository(db, limit, offset)

def deletar_produto_service(db: Session, id: int):
    produto = buscar_produto_por_id_service(db, id)
    deletar_produto_repository(db, produto)
    db.commit()
    