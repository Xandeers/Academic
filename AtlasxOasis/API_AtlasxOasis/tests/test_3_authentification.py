from .client import client
from tests.payload import general_customer_payload


class TestDB:

    def test_login_client(self, test_customer):
        
        login = {
            "username": general_customer_payload['email'],
            "password": general_customer_payload['token']
        }

        #failed connection
        response = client.post("/auth/login", json={
            "username": "fake@gmail.com",
            "password": "password"
        })
        
        assert(response.status_code == 422)

        response = client.post("/auth/login", data=login)
        print(response)
        assert(response.status_code == 200)

