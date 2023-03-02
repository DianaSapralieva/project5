from jose import jwt, JWTError
from ..schemas import Token
from fastapi import HTTPException, status

#openssl rand -hex 32
SERVER_KEY = "39185de17e18c2a257eb83977a759cc6fa368f307ccae643884f069e71988033"
ALGORITHM="HS256"

#function generate token
def generate_token(id:int ):
    payload={"user_id":id}
    encoded_jwt=jwt.encode(payload,SERVER_KEY,algorinthm=ALGORITHM)
    return Token(access_token=encoded_jwt,token_type="Bearer")

#function to decode the token
def decode_token(provided_token):
    try:
        payload=jwt.decode(provided_token,SERVER_KEY,algorinthms=[ALGORITHM])
        decoded_id=payload["user_id"]
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate token", headers={"WWW-Authenticate":"Bearer"}
        )   
    return decoded_id


