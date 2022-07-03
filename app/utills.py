from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password:str):
    return pwd_context.hash(password)



def verify (plain_text, hashed_password):
    return pwd_context.verify(plain_text,hashed_password)

