from tests.client import client


#tests corrects mais routes pas implémentés

class TestFollow():

    def test_follow_event(self, test_event, auth_customer_headers):

        response = client.post(
            f"/events/{test_event['id_event']}/like",
            headers= auth_customer_headers
        )
        assert response.status_code == 201

    def test_unfollow_event(self, test_event, auth_customer_headers):
        
        response = client.delete(
            f"/events/{test_event['id_event']}/like",
            headers=auth_customer_headers
        )

        assert response.status_code == 200

    def test_follow_user(self, auth_customer_headers, test_organizer): 

        response = client.post(
            f"/users/{test_organizer['id_organizer']}/follow",
            json={"status_follow": "active"},
            headers=auth_customer_headers
        )

        assert response.status_code == 201

    def test_get_followers(self, test_organizer):

        response = client.get(f"/users/{test_organizer['id_organizer']}/followers")

        assert response.status_code, 200
        assert isinstance(response.json(), list)

    def test_get_followed(self, test_customer):

        response = client.get(f"/users/{test_customer['id_customer']}/followed")

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_unfollow_user(self, auth_customer_headers, test_organizer):

        response = client.delete(
            f"/users/{test_organizer['id_organizer']}/unfollow",
            headers=auth_customer_headers
        )

        assert response.status_code == 200