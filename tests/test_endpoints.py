import pytest
from sqlalchemy.orm.session import Session

from schemas.accounts import AccountCreate
from tests.test_main import client

# uv run -m pytest -v --cov=routes --cov-report term-missing
# uv run -m pytest -v -s
# uv run -m pytest -v


def test_create_new_account(test_db: Session):
    account_data = AccountCreate(
        username="Marília", balance=254.25, password="21452145"
    )
    response = client.post("/conta/criar", json=account_data.model_dump())

    assert response.status_code == 200
    assert account_data.username == response.json()["username"]
    assert "account_number" in response.json()


def test_create_new_account_inssuficient_passwd_caracters(test_db: Session):
    account_data = AccountCreate(username="Marília", balance=254.25, password="12545")
    response = client.post("/conta/criar", json=account_data.model_dump())

    assert response.status_code == 409


def test_create_duplicated_account(test_db: Session):
    account_data = AccountCreate(
        username="Marília", balance=254.25, password="548624896"
    )
    response = client.post("/conta/criar", json=account_data.model_dump())
    response_2 = client.post("/conta/criar", json=account_data.model_dump())

    assert response.status_code == 200
    assert response_2.status_code == 409


def test_login_success(test_db: Session):
    account_data = AccountCreate(
        username="Marília", balance=254.25, password="21452145"
    )
    response = client.post("/conta/criar", json=account_data.model_dump())
    assert response.status_code == 200

    login_data = {
        "username": str(response.json()["account_number"]),
        "password": str(account_data.password),
    }
    login = client.post(
        "/login",
        data=login_data,
    )
    assert login.status_code == 200
    data = login.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_account_failed(test_db: Session):
    account_data = AccountCreate(
        username="Marília", balance=254.25, password="21452145"
    )
    response = client.post("/conta/criar", json=account_data.model_dump())
    assert response.status_code == 200

    login_data = {
        "username": "89495",
        "password": str(account_data.password),
    }
    login = client.post(
        "/login",
        data=login_data,
    )
    assert login.status_code == 401


def test_login_password_failed(test_db: Session):
    account_data = AccountCreate(
        username="Marília", balance=254.25, password="21452145"
    )
    response = client.post("/conta/criar", json=account_data.model_dump())
    assert response.status_code == 200

    login_data = {
        "username": str(response.json()["account_number"]),
        "password": "849846545598",
    }
    login = client.post(
        "/login",
        data=login_data,
    )
    assert login.status_code == 401


def test_login_password_and_account_failed(test_db: Session):
    account_data = AccountCreate(
        username="Marília", balance=254.25, password="21452145"
    )
    response = client.post("/conta/criar", json=account_data.model_dump())
    assert response.status_code == 200

    login_data = {
        "username": "98498",
        "password": "984949858",
    }
    login = client.post(
        "/login",
        data=login_data,
    )
    assert login.status_code == 401


def test_read_users_me(test_db):
    password = "123456"
    account_data = account_data = {
        "username": "Clebinho",
        "balance": 5000,
        "password": password,
    }
    create_account = client.post("conta/criar", json=account_data)
    account_number = create_account.json()["account_number"]

    login_data = {
        "username": str(account_number),
        "password": str(account_data["password"]),
    }
    credentials = client.post("/login", data=login_data)
    token = credentials.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "Clebinho"
    assert response.json()["account_number"] == account_number


def test_read_users_me_without_token(test_db):
    response = client.get("/me")
    assert response.status_code == 401


@pytest.mark.parametrize(
    "balance_test, assert_status", [(-200.25, 422), (-0.01, 422), (0, 422)]
)
def test_create_account_invalid_balance(test_db: Session, balance_test, assert_status):
    payload = {"username": "Teste", "balance": balance_test}
    response = client.post("/conta/criar", json=payload)
    assert response.status_code == assert_status


@pytest.mark.parametrize(
    "payload, status_code, detail",
    [
        ({"username": "Marilia", "balance": 0}, 422, "detail"),
        ({"username": "", "balance": 500}, 422, "detail"),
        ({"username": "", "balance": -500}, 422, "detail"),
        ({"username": "", "balance": 0}, 422, "detail"),
    ],
)
def test_invalid_payload(test_db, payload, status_code, detail):
    response = client.post("/conta/criar", json=payload)
    assert response.status_code == status_code
    print(response.text)
    assert detail in response.text


def test_get_balance_valid_account(test_db):
    account_data = AccountCreate(
        username="Marília", balance=254.25, password="6548665598"
    )
    new_account = client.post("/conta/criar", json=account_data.model_dump())
    account_number = new_account.json()["account_number"]

    response = client.get("/conta", params={"account_number": account_number})
    assert response.status_code == 200
    assert "balance" in response.json()


@pytest.mark.parametrize(
    "account_number, status_code", [(5425, 404), ("qweq", 422), ("", 422), (None, 422)]
)
def test_get_balance_invalid_account(test_db, account_number, status_code):
    response = client.get("/conta", params={"account_number": account_number})
    assert response.status_code == status_code
