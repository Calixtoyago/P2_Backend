# API de Produtos

API REST para gerenciamento de produtos, desenvolvida com **FastAPI**, **SQLAlchemy ORM**, **PostgreSQL**, **Alembic** e **Pytest**.

O projeto foi estruturado com foco em:

- separação de responsabilidades
- persistência relacional
- migrations versionadas
- ambiente isolado para testes
- automação com Docker

---

# Objetivo

A API permite:

- cadastrar produtos
- listar produtos
- buscar produto por ID
- remover produtos

Cada produto possui:

- `id`
- `nome`
- `preco`
- `estoque`
- `created_at`

---

# Stack utilizada

## Backend

- Python 3.13
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic

## Banco de dados

- PostgreSQL 15

## Testes

- Pytest
- TestClient (FastAPI)

## Infraestrutura

- Docker
- Docker Compose

---

# Arquitetura do projeto

```text
.
├── app/
│   ├── core/
│   │   └── exceptions.py
│   ├── models.py
│   │   └── models.py
│   ├── reporitory/
│   │   └── produto_repository.py
│   ├── routers/
│   │   └── produto_router.py
│   ├── schemas/
│   │   └── produto_schema.py
│   ├── services/
│   │   └── produto_service.py
│   └── main.py
│
├── migrations/
│   ├── versions/
│   └── env.py
│   └──README.md
│   └──script.py.mako
│
├── tests/
│   ├── __init__.py
│   └── test_produtos.py
│
├── .env.example
├── alembic.init 
├── conftest.py
├── database.py
├── docker-compose.yml
├── Dockerfile
├── pytest.py
├── README.md
├── requirements.txt
```

---

# Estrutura lógica

O projeto segue separação por camadas:

## Router

Responsável por:

- definir endpoints
- receber requests
- devolver responses

Exemplo:

```python
@app.post("/produtos/")
```

---

## Service

Responsável pela regra de negócio:

- criação
- consulta
- remoção

Evita lógica no router.

---

## Models

Representação ORM da tabela:

```python
class Produto(Base)
```

---

## Schemas

Validação de entrada e serialização de saída com Pydantic.

---

# Banco de dados

O projeto possui **dois bancos separados**.

## Desenvolvimento

Serviço:

```text
db_dev
```

Porta:

```text
5432
```

Persistência:

```text
Volume nomeado
```

---

## Testes

Serviço:

```text
db_test
```

Porta:

```text
5433
```

Persistência:

```text
tmpfs (descartável)
```

Isso garante isolamento entre ambiente real e ambiente de testes.

---

# Como executar o projeto

## 1. Clonar repositório

```bash
git clone <url-do-repositorio>
cd nome-do-projeto
```

---

## 2. Subir containers

```bash
docker compose up -d --build
```

Verificar:

```bash
docker ps
```

Saída esperada:

```text
api
db_dev
db_test
```

---

# Executando migrations

## Criar migration

```bash
docker compose exec api alembic revision --autogenerate -m "criacao inicial"
```

---

## Aplicar migration

```bash
docker compose exec api alembic upgrade head
```

---

# Executando a API

A API estará disponível em:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Redoc:

```text
http://localhost:8000/redoc
```

---

# Endpoints

---

## Criar produto

### Request

```http
POST /produtos/
```

Body:

```json
{
  "nome": "Notebook",
  "preco": 3500.00,
  "estoque": 10
}
```

Response:

```json
{
  "id": 1,
  "nome": "Notebook",
  "preco": 3500.00,
  "estoque": 10
}
```

---

## Listar produtos

### Request

```http
GET /produtos/
```

Response:

```json
[
  {
    "id": 1,
    "nome": "Notebook",
    "preco": 3500.00,
    "estoque": 10
  }
]
```

---

## Buscar produto por ID

### Request

```http
GET /produtos/id/1
```

Response:

```json
{
  "id": 1,
  "nome": "Notebook",
  "preco": 3500.00,
  "estoque": 10
}
```

---

## Deletar produto

### Request

```http
DELETE /produtos/1
```

Response:

```http
204 No Content
```

---

# Testes automatizados

Os testes estão em:

```text
tests/test_produtos.py
```

Cobertura:

- listar produtos com banco vazio
- criar produto
- verificar persistência
- buscar produto por ID
- buscar ID inexistente
- deletar produto
- confirmar remoção
- deletar inexistente
- payload inválido
- isolamento entre execuções

Total:

```text
12 testes
```

---

# Como subir banco de testes

O banco de testes sobe junto com:

```bash
docker compose up -d
```

Mas pode subir isoladamente:

```bash
docker compose up -d db_test
```

Porta:

```text
5433
```

---

# Executando os testes

Comando oficial:

```bash
docker compose exec api pytest -v
```

Com cobertura:

```bash
docker compose exec api pytest --cov=app -v
```

---

# Saída esperada do pytest

```text
============================= test session starts =============================

collected 12 items

tests/test_produtos.py::test_listar_produtos_vazio PASSED
tests/test_produtos.py::test_criar_produto PASSED
tests/test_produtos.py::test_criar_produto_e_listar PASSED
tests/test_produtos.py::test_buscar_produto_por_id PASSED
tests/test_produtos.py::test_buscar_produto_id_inexistente PASSED
tests/test_produtos.py::test_deletar_produto PASSED
tests/test_produtos.py::test_deletar_produto_e_confirmar_remocao PASSED
tests/test_produtos.py::test_deletar_produto_inexistente PASSED
tests/test_produtos.py::test_payload_invalido[payload0] PASSED
tests/test_produtos.py::test_payload_invalido[payload1] PASSED
tests/test_produtos.py::test_payload_invalido[payload2] PASSED
tests/test_produtos.py::test_banco_isolado PASSED

============================= 12 passed =============================
```

---

# Como funciona o isolamento entre testes

O isolamento é implementado pelo `conftest.py`.

A fixture `client` executa:

## Antes de cada teste

Cria as tabelas:

```python
Base.metadata.create_all(bind=engine_test)
```

Substitui a dependência:

```python
app.dependency_overrides[get_db]
```

Assim os testes usam apenas:

```text
db_test
```

---

## Depois de cada teste

Apaga tudo:

```python
Base.metadata.drop_all(bind=engine_test)
```

Fluxo:

```text
Início do teste
↓
Cria schema
↓
Executa teste
↓
Remove schema
↓
Próximo teste inicia limpo
```

Isso garante:

- independência
- previsibilidade
- ausência de dados residuais

---

# Variáveis de ambiente

Exemplo:

```env
DATABASE_DEV_URL=postgresql://postgres:1234@db_dev:5432/produtos_db
DATABASE_TEST_URL=postgresql://postgres:1234@db_test:5432/test_db

POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234

PORT=8000
```

---

# Observações técnicas

## Dentro do Docker:

Use:

```text
db_dev:5432
db_test:5432
```

---

## Fora do Docker:

Use:

```text
localhost:5432
localhost:5433
```

Exemplo:

DBeaver → `localhost`

Nunca:

```text
db_dev
```

porque isso só existe na rede Docker.

---

# Autor

Projeto desenvolvido para fins acadêmicos na disciplina de backend, aplicando conceitos de:

- APIs REST
- ORM
- migrations
- testes automatizados
- isolamento de banco
- infraestrutura com containers
