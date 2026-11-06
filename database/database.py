
import os
from typing import Generator

from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv(".env.local")

# SQLite local por defecto.
# Neon PostgreSQL cuando DATABASE_URL esté configurada.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///biblioteca.db"
)

# Compatibilidad con URLs PostgreSQL.
# Utilizar psycopg 3 para las conexiones PostgreSQL.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+psycopg://",
        1
    )

elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

# Configuración específica según la base de datos.
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=False
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
