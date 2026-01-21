from schemas.accounts import AccountCreate
from tests.test_main import client


# uv run -m pytest -v
def test_create_new_account(test_db):
    account_data = AccountCreate(username="Marília", balance=254.25)
    response = client.post("/conta/criar", json=account_data.model_dump())

    assert response.status_code == 200


def test_create_duplicated_account(test_db):
    account_data = AccountCreate(username="Marília", balance=254.25)
    response = client.post("/conta/criar", json=account_data.model_dump())
    response_2 = client.post("/conta/criar", json=account_data.model_dump())

    assert response.status_code == 200
    assert response_2.status_code == 409


def test_create_account_negative_value(test_db):
    account_data = {"username": "Marília", "balance": -254.25}
    response = client.post("/conta/criar", json=account_data)
    assert response.status_code == 422
