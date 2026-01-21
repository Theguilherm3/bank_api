import pytest
from sqlalchemy.orm.session import Session

from schemas.accounts import AccountCreate
from tests.test_main import client

# uv run -m pytest -v --cov=routes --cov-report term-missing
# uv run -m pytest -v -s
# uv run -m pytest -v


def test_create_new_account(test_db: Session):
    account_data = AccountCreate(username="Marília", balance=254.25)
    response = client.post("/conta/criar", json=account_data.model_dump())

    assert response.status_code == 200


def test_create_duplicated_account(test_db: Session):
    account_data = AccountCreate(username="Marília", balance=254.25)
    response = client.post("/conta/criar", json=account_data.model_dump())
    response_2 = client.post("/conta/criar", json=account_data.model_dump())

    assert response.status_code == 200
    assert response_2.status_code == 409


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
    account_data = AccountCreate(username="Marília", balance=254.25)
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
