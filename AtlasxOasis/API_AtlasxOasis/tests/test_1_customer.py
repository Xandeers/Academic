from unittest import TestCase

from typing_extensions import Any
from src.api_atlaxoasis_2026.schema.customer import CustomerSchema
from .client import client, get_auth_headers
from tests.payload import general_customer_payload

class TestCustomer(TestCase):
    
    customer = {}

    def setUp(self):
        # On définit toutes les données nécessaires, y compris les champs manquants
        self.customer_payload = general_customer_payload

    def test_1_create_customer(self):
        # Utilise .model_dump() pour envoyer un dictionnaire propre à l'API
        response = client.post("/customers/", json=self.customer_payload)
        self.assertEqual(response.status_code, 200)
        TestCustomer.customer = response.json()
        self.assertIn("id_customer", TestCustomer.customer)
        self.assertEqual(TestCustomer.customer["username"], self.customer_payload["username"])

    def test_2_get_all_customers(self):
        response = client.get("/customers/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_3_get_customer_by_id(self):

        # Récupération
        response = client.get(f"/customers/{TestCustomer.customer['id_customer']}")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data, TestCustomer.customer)
    
    def test_4_update_customer(self):
        
        response = client.get(f"/customers/{TestCustomer.customer['id_customer']}")
        self.assertEqual(response.status_code, 200, response.json())
        
        data = response.json()
        
        header = get_auth_headers(email= data['email'], password= general_customer_payload['token'])
        
        
        response = client.put("/customers/", json={"username" : "test_update"}, headers=header)
        self.assertEqual(response.status_code, 200)
        
        response = client.get(f"/customers/{TestCustomer.customer['id_customer']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "test_update")
        
        
    def test_5_delete_customer(self):

        # Suppression
        delete_resp = client.delete(f"/customers/{TestCustomer.customer['id_customer']}")
        self.assertEqual(delete_resp.status_code, 200)

        # Vérification (doit retourner 404)
        get_resp = client.get(f"/customers/{TestCustomer.customer['id_customer']}")
        self.assertEqual(get_resp.status_code, 404)