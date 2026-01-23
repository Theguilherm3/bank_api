from fastapi.testclient import TestClient


def create_account(client: TestClient, username, balance, password="1234567"):
    payload = {"username": username, "balance": balance, "password": password}

    response = client.post("/conta/criar", json=payload)
    assert response.status_code == 200
    assert response.json()["account_number"]
    return response.json()["account_number"]


def login(client: TestClient, account_number, password):
    login_data = {"username": account_number, "password": str(password)}

    response = client.post("/login", data=login_data)
    assert response.status_code == 200
    assert response.json()["access_token"]
    return response.json()["access_token"]


def create_account_and_login(client: TestClient, username, balance, password="1234567"):
    account_number = create_account(client, username, balance, password)
    token = login(client, account_number, password)

    final_token = {"token": token, "sub": account_number}
    return final_token
