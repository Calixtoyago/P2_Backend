import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from database import Base, get_db

DATABASE_TEST_URL = os.getenv(
    "DATABASE_TEST_URL",
    "postgresql://postgres:1234@localhost:5433/test_db"
)

engine_test = create_engine(DATABASE_TEST_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine_test)

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture()
def produto_existente(client):
    payload = {
        "nome": "Notebook",
        "preco": 3500.00,
        "estoque": 10
    }

    response = client.post("/produtos/", json=payload)

    return response.json()