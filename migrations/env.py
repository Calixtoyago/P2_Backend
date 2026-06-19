import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from alembic import context

# Garante que a raiz do projeto (/app) esteja no path para os imports abaixo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Engine e Base já configuradas pela aplicação (a engine usa a URL do .env)
from database import Base, engine
from app.models.models import Produto  # noqa: F401 — registra a tabela no metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=engine.url.render_as_string(hide_password=False),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()