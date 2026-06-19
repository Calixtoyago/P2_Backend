from fastapi import FastAPI
from app.router.produto_router import router as produto_router
from app.core.exceptions import BusinessError, business_error_handler
# Inicializa a aplicação
app = FastAPI(
    title="API - Sistema Bancário",
    description="API para gerenciamento de contas, cartões e transações.",
    version="1.0.0"
)

app.add_exception_handler(BusinessError, business_error_handler)

app.include_router(produto_router)

# Cria uma rota raiz só para testar se está tudo funcionando
@app.get("/")
def health_check():
    return {
        "status": "online",
        "mensagem": "A API da P2 está rodando perfeitamente!"
    }