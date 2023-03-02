from passlib.context import CryptContext

#initilize the crypto context 
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pass(password: str):
    return pwd_context.hash(password) #hash_password 

def verify_passsword(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)#if passwords are matching 