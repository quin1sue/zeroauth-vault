from datetime import datetime, timedelta
from jose import jwt 
from src.config import settings

def create_access_token(data: dict):
    to_encode = data.copy()

    # set expiration time of auth
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    # sign the token using the secret key
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

    return encoded_jwt