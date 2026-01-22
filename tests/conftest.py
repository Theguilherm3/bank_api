from pytest import fixture
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db.base import Base
from db.session import get_db
from tests.test_main import app

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestSession = sessionmaker(bind=engine)

# StaticPool é importante pro banco de dados se manter o mesmo
# enquanto a engine estiver ativa, ja que estamos usando memoria


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
