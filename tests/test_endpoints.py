import pytest
from sqlalchemy.orm.session import Session

from schemas.accounts import AccountCreate
from tests.test_main import client


# uv run -m pytest -v --cov=routes --cov-report term-missing
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
