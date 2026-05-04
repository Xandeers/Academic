from tests.client import client
from tests.payload import general_category_payload

class TestCategory:
    
    category = {}
    
    def test_create_category(self):
        response = client.post("/category", json=general_category_payload)
        
        data = response.json()
        print(data)
        
        assert data["label"] == general_category_payload["label"]
        
        TestCategory.category = data
    
    def test_get_category(self):
        response = client.get(f"/category/{TestCategory.category['id_category']}")
        
        assert response.json()["label"] == general_category_payload["label"]
        
    def test_get_all_category(self):
        response = client.get("/category/")
        
        data = response.json()
        
        print(data)
        
        assert TestCategory.category in data
    
    def test_delete_category(self):
        response = client.delete(f"/category/{TestCategory.category['id_category']}")
        
        assert response.status_code == 200
        
        response = client.get(f"/category/{TestCategory.category['id_category']}")
        
        assert response.status_code == 404
        
            
        
        
        