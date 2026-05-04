from unittest import TestCase
from tests.client import client
from tests.payload import general_organizer_payload


class TestOrganizer(TestCase):
    
    organizer = {}

    def setUp(self):
        # On définit toutes les données nécessaires, y compris les champs manquants
        self.customer_payload = general_organizer_payload

    def test_1_create_organizer(self):
        # Utilise .model_dump() pour envoyer un dictionnaire propre à l'API
        response = client.post("/organizers/", json=self.customer_payload)
        self.assertEqual(response.status_code, 200)
        TestOrganizer.organizer = response.json()
        self.assertIn("id_organizer", TestOrganizer.organizer)
        self.assertEqual(TestOrganizer.organizer["username"], self.customer_payload["username"])

    def test_2_get_all_organizers(self):
        response = client.get("/organizers/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_3_get_organizer_by_id(self):

        # Récupération
        response = client.get(f"/organizers/{TestOrganizer.organizer['id_organizer']}")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data, TestOrganizer.organizer)
        
    def test_4_delete_organizer(self):

        # Suppression
        delete_resp = client.delete(f"/organizers/{TestOrganizer.organizer['id_organizer']}")
        self.assertEqual(delete_resp.status_code, 200)

        # Vérification (doit retourner 404)
        get_resp = client.get(f"/organizers/{TestOrganizer.organizer['id_organizer']}")
        self.assertEqual(get_resp.status_code, 404)

