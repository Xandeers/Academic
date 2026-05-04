from bcrypt import hashpw, gensalt, checkpw 


def hash_password(password : str) -> str :
    return hashpw(password.encode("Utf-8"),gensalt()).decode("utf-8")

def check_password(password1:str, password2:str) -> bool : 
        return checkpw(password1.encode("utf-8"),password2.encode("utf-8"))