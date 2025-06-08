from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    hashed_password = pwd_context.hash(password)

    return hashed_password

def authenticate(plain_password:str,hashed_password:str):
    # new_hashed_password = hash(plain_password)

    # if new_hashed_password == hashed_password:
    #     return True
    # else:
    #     return False

    return pwd_context.verify(plain_password,hashed_password)