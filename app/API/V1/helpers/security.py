from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext

from app.settings import (
    SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_KEY,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    RECOVERY_KEY,
    RECOVERY_TOKEN_EXPIRE_MINUTES,
)

# Encriptador de la pass en la db al hacer login
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


# Creación de token de acceso
def create_access_token(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Creación de token de refresco
def create_refresh_token(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, REFRESH_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Creación de token de recuperación de contraseña
def create_recovery_token(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(minutes=RECOVERY_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, RECOVERY_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Compara de contraseña para login
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Encriptador de contraseña
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Decodificador de token de login
def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return (
            decoded_token
            if decoded_token["exp"] >= datetime.utcnow().timestamp()
            else None
        )
    except Exception as e:
        print(e)
        return {}


# Decodificador de token de refresco
def decodeRefreshJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, REFRESH_KEY, algorithms=ALGORITHM)
        return (
            decoded_token
            if decoded_token["exp"] >= datetime.utcnow().timestamp()
            else None
        )
    except Exception as e:
        print(e)
        return {}


# Decodificador de token de recuperación de contraseña
def decodeRecoverJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, RECOVERY_KEY, algorithms=ALGORITHM)
        return (
            decoded_token
            if decoded_token["exp"] >= datetime.utcnow().timestamp()
            else None
        )
    except Exception as e:
        print(e)
        return {}
