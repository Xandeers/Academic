from src.api_atlaxoasis_2026.security.jwt import *



user_info_test = {"username": "test", "role": "admin", "user_id": 42}


def test_jwt_creation_ok():

    token = create_jwt(data=user_info_test)

    assert token is not None
    assert isinstance(token,str)

    decoded_token= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded_token["username"] == "test"
    assert decoded_token["role"] == "admin"
    assert decoded_token["user_id"] == 42
    assert "exp" in decoded_token