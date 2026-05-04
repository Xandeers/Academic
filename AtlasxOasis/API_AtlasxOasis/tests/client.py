from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def get_auth_headers(email: str, password: str):
    """Se connecte une fois et retourne les headers avec le token."""
    response = client.post("/auth/login", data={
        "username": email,
        "password": password
    })
    assert response.status_code == 200, f"Connextion echoué {response.json()}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}