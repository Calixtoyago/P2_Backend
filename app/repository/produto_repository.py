from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.models import Produto

def criar_produto_repository(db: Session, produto):
    novo_produto = Produto(
        nome=produto.nome,
        preco=produto.preco,
        estoque=produto.estoque,
        # ativo - é TRUE por padrão no models.py
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

def listar_produtos_repository(db: Session, limit: int, offset: int):
    query = select(Produto).limit(limit).offset(offset)
    return db.execute(query).scalars().all()

def buscar_produto_por_id_repository(db: Session, id: int):
    query = select(Produto).where(Produto.id == id)
    return db.execute(query).scalar_one_or_none()

def deletar_produto_repository(db: Session, produto: Produto):
    return db.delete(produto)

def buscar_produto_por_nome_repository(db: Session, nome: str):
    query = select(Produto).where(Produto.nome == nome)
    return db.execute(query).scalar_one_or_none()