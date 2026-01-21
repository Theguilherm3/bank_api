from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base import Base
from db.session import get_db
from tests.test_main import app

DATABASE_URL = "sqlite:///./test_objectivebank.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

TestSession = sessionmaker(bind=engine)


@fixture
def test_db():
    print("Criando tabelas")
    Base.metadata.create_all(bind=engine)
    db = TestSession()

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield db
    finally:
        print("Deletando dados")

        app.dependency_overrides.clear()
        db.close()
        Base.metadata.drop_all(bind=engine)
