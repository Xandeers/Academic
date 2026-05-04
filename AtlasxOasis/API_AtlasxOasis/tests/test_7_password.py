from src.api_atlaxoasis_2026.security.hashing import hash_password, check_password



def test_password_hashing_OK():
    
    my_password = "myPassword"

    hash = hash_password(my_password)

    assert my_password !=  hash
    assert hash.startswith("$2b$")
    assert check_password(my_password, hash) is True


def test_wrong_password():
    
    my_password = "myPassword"
    other_password = "Wrong_Password"
    hash = hash_password(my_password)

    assert check_password(other_password,hash) is False

