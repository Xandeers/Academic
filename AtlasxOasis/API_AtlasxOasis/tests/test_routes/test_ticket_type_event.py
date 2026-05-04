from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime

from main import app

from model import EventDB, TicketTypeEventDB
from security.permissions import verify_event_owner, get_user_id
from unittest.mock import MagicMock
from routes.ticket_type_event import SessionDependency

client = TestClient(app)

async def mock_verify_event_owner():
    """Ce faux vigile renvoie un événement valide basé sur ton EventDB."""
    return EventDB(
        id_event=1, 
        id_organizer=42, 
        name="Concert de Test",
        start_date=datetime.now(),
        end_date=datetime.now(),
        creation_date=datetime.now(),
        event_status="published",
        max_capacity=500,
        description="Un événement généré pour les tests SonarQube"
        
    )

async def mock_get_user_id():
    """Ce faux vigile remplace la vérification du token JWT"""
    return 42

app.dependency_overrides[verify_event_owner] = mock_verify_event_owner
app.dependency_overrides[get_user_id] = mock_get_user_id



@patch("routes.ticket_type_event.update_ticket_type_event_db")
def test_patch_ticket_type_for_event_success(mock_update_service):
    
    #On prépare ce que le service simulé doit répondre
    mock_update_service.return_value = TicketTypeEventDB(
        id_ticket_type=2,
        id_event=1,
        price="15.00",
        label="VIP",
        description="Nouveau prix promo",
        quantity=100
    )


    # On envoie la vraie requête HTTP (normalement pas de verif de token dans le test)
    payload_json = {
        "price": "15.00",
        "description": "Nouveau prix promo"
    }
    
    # La requête PATCH sur /ticket_type_event/1/2
    response = client.patch("/ticket_type_event/1/2", json=payload_json)

    
    
    # verif route répond bien un succès (200)
    assert response.status_code == 200
    
    # Verif que le JSON renvoyé contient bien la modification
    data = response.json()
    assert data["price"] == "15.00"
    assert data["description"] == "Nouveau prix promo"
    assert data["label"] == "VIP" 
    
    
    mock_update_service.assert_called_once()


