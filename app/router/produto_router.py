from fastapi import APIRouter, Depends, Response
from app.schemas.produto_schema import ProdutoCreate, ProdutoResponse
from app.services.produto_service import *
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/produtos", tags=["Produtos"])

#POST - criar produto
@router.post("/", response_model=ProdutoResponse)
def criar_produto_router(produto: ProdutoCreate, db: Session = Depends(get_db)):
    return criar_produto_service(db, produto)

#GET - listar produtos
@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos_router(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    return listar_produtos_service(db, limit, offset)

#GET - buscar produto por id
@router.get("/id/{id}", response_model=ProdutoResponse)
def buscar_produto_por_id_router(id: int, db: Session = Depends(get_db)):
    return buscar_produto_por_id_service(db, id)

#GET - buscar produto por nome
@router.get("/nome/{nome}", response_model=ProdutoResponse)
def buscar_produto_por_id_router(nome: str, db: Session = Depends(get_db)):
    return buscar_produto_por_nome_service(db, nome)

#DELETE - deletar produto pelo id   
@router.delete("/{id}", status_code=204)
def deletar_produto_router(id: int, db: Session = Depends(get_db)):
    deletar_produto_service(db, id)
    return Response(status_code=204)
