from tests.client import client
from tests.payload import general_category_payload

event_data = {
    "name": "Test Event",
    "start_date": "2026-01-01T10:00:00",
    "end_date": "2026-01-01T12:00:00",
    "created_date": "2026-01-01T09:00:00",
    "event_status": "published",
    "max_capacity": 100,
    "description": "Test description",
    "metadata": {}
}

class TestEvent():

    def test_1_create_event(self, auth_organizer_headers):
        global event_data
        response = client.post("/events/", json=event_data, headers=auth_organizer_headers)
        assert response.status_code == 200
        event_data = response.json()
        assert "id_event" in event_data

    def test_2_get_events(self):
        response = client.get("/events/")
        assert response.status_code == 200, response.text
        assert response.json(), list

    def test_3_get_event_by_id(self):
        event_id = event_data["id_event"]

        response = client.get(f"/events/{event_id}")
        assert response.status_code == 200, response.text
        assert response.json()["id_event"] == event_id

    def test_4_update_event(self, auth_organizer_headers):
        event_id = event_data["id_event"]

        response = client.put(f"/events/{event_id}", json={"name": "Updated Event"}, headers= auth_organizer_headers)
        assert response.status_code == 201, response.text
        
    def test_5_update_inexisting_event(self, auth_organizer_headers):
        event_id = 0
        
        response = client.put(f"/events/{event_id}", json={"name": "Updated Event"}, headers= auth_organizer_headers)
        assert response.status_code == 404
    
    def test_6_add_category(self, test_category):
        event_id = event_data["id_event"]
        category_id = test_category["id_category"]
        
        response = client.post(f"/events/{event_id}/category/{category_id}")
        assert response.status_code == 200
        
    def test_7_add_location(self, test_location):
        event_id = event_data["id_event"]
        location_id = test_location["id_location"]
        
        response = client.post(f"/events/{event_id}/location/{location_id}")
        assert response.status_code == 200
        
    
    def test_8_add_media(self, test_media):
        event_id = event_data["id_event"]
        media_id = test_media["id_media"]
        
        response = client.post(f"/events/{event_id}/media/{media_id}")
        assert response.status_code == 200
    
    # def test_8_add_promotion(self, test_promotion):
    #     event_id = event_data["id_event"]
    #     promotion_id = test_promotion["id_media"]
        
    #     response = client.post(f"/events/{event_id}/promotion/{promotion_id}")
    #     assert response.status_code == 200
    

    def test__delete_event(self):
        event_id = event_data["id_event"]

        response = client.delete(f"/events/{event_id}")
        assert response.status_code == 200, response.text