import pytest
from decimal import Decimal


def test_listar_produtos_vazio(client):
    response = client.get("/produtos/")
    assert response.status_code == 200
    assert response.json() == []


def test_criar_produto(client):
    payload = {
        "nome": "Mouse",
        "preco": 100,
        "estoque": 20
    }

    response = client.post("/produtos/", json=payload)

    assert response.status_code == 200
    assert response.json()["nome"] == "Mouse"


def test_criar_produto_e_listar(client):
    client.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 200,
        "estoque": 5
    })

    response = client.get("/produtos/")

    assert len(response.json()) == 1


def test_buscar_produto_por_id(client, produto_existente):
    produto_id = produto_existente["id"]

    response = client.get(f"/produtos/id/{produto_id}")

    assert response.status_code == 200
    assert response.json()["id"] == produto_id


def test_buscar_produto_id_inexistente(client):
    response = client.get("/produtos/id/999")

    assert response.status_code == 404


def test_deletar_produto(client, produto_existente):
    produto_id = produto_existente["id"]

    response = client.delete(f"/produtos/{produto_id}")

    assert response.status_code == 204


def test_deletar_produto_e_confirmar_remocao(client, produto_existente):
    produto_id = produto_existente["id"]

    client.delete(f"/produtos/{produto_id}")

    response = client.get(f"/produtos/id/{produto_id}")

    assert response.status_code == 404


def test_deletar_produto_inexistente(client):
    response = client.delete("/produtos/999")

    assert response.status_code == 404


@pytest.mark.parametrize("payload", [
    {"nome": "", "preco": 100, "estoque": 1},
    {"nome": "Produto", "preco": -10, "estoque": 1},
    {"nome": "Produto", "preco": 100, "estoque": -1},
])
def test_payload_invalido(client, payload):
    response = client.post("/produtos/", json=payload)

    assert response.status_code in [422, 500]


def test_banco_isolado(client):
    response = client.get("/produtos/")

    assert response.json() == []