# conftest.py
import pytest
from .client import client, get_auth_headers
from tests.payload import  general_category_payload, general_customer_payload, general_location_payload, general_media_payload, general_organizer_payload, general_event_payload, general_promotion_payload


@pytest.fixture(scope="session")
def test_customer():
    """Crée un customer avant les tests, le supprime après (même en cas d'erreur)."""
    
    # ── SETUP ──────────────────────────────────────────────
    payload = general_customer_payload
    response = client.post("/customers/", json=payload)
    assert response.status_code == 200, f"Création échouée : {response.json()}"
    
    customer = response.json()
    
    yield customer  # ← Les tests reçoivent le customer ici
    
    # ── TEARDOWN (toujours exécuté) ─────────────────────────
    client.delete(f"/customers/{customer['id_customer']}")

@pytest.fixture(scope="session")
def test_organizer():
    """Crée un organizer avant les tests, le supprime après (même en cas d'erreur)."""
    
    # ── SETUP ──────────────────────────────────────────────
    payload = general_organizer_payload
    response = client.post("/organizers/", json=payload)
    assert response.status_code == 200, f"Création échouée : {response.json()}"
    
    organizer = response.json()
    
    yield organizer  # ← Les tests reçoivent le customer ici
    
    # ── TEARDOWN (toujours exécuté) ─────────────────────────
    client.delete(f"/organizers/{organizer['id_organizer']}")
    
@pytest.fixture(scope="session")
def auth_customer_headers(test_customer):
    """Récupère le token une seule fois pour toute la session."""
    return get_auth_headers(email= general_customer_payload['email'], password= general_customer_payload['token'])
    
@pytest.fixture(scope="session")
def auth_organizer_headers(test_organizer):
    """Récupère le token une seule fois pour toute la session."""
    return get_auth_headers(email= general_organizer_payload['email'], password= general_organizer_payload['token'])
    
@pytest.fixture(scope="session")
def test_event(auth_organizer_headers):
    payload = general_event_payload
    response = client.post("/events/", json=payload, headers=auth_organizer_headers)
    assert response.status_code == 200, f"Création échouée : {response.json()}"
    
    event = response.json()
    
    yield event
    
    client.delete(f"/events/{event['id_event']}")
    
@pytest.fixture(scope="session")
def test_category():
    payload = general_category_payload
    response = client.post("/category/", json=payload)
    assert response.status_code == 200, f"Création échouée : {response.json()}"
    
    category = response.json()
    
    yield category
    
    client.delete(f"/events/{category['id_category']}")

@pytest.fixture(scope="session")
def test_location():
    payload = general_location_payload
    response = client.post("/locations/", json=payload)
    assert response.status_code == 200, f"Création échouée : {response.json()}"
    
    location = response.json()
    
    yield location
    
    client.delete(f"/location/{location['id_location']}")
    
@pytest.fixture(scope="session")
def test_media(auth_organizer_headers):
    payload = general_media_payload
    response = client.post("/media/", json=payload, headers=auth_organizer_headers)
    assert response.status_code == 200, f"Création échouée : {response.json()}"
    
    media = response.json()
    
    yield media
    
    client.delete(f"/media/{media['id_media']}")

@pytest.fixture(scope="session")
def test_promotion():
    payload = general_promotion_payload
    response = client.post("/promotions/", json=payload)
    assert response.status_code == 200, f"Création échouée : {response.json()}"
    
    promotion = response.json()
    
    yield promotion
    
    client.delete(f"/promotions/{promotion['id_promotion']}")

