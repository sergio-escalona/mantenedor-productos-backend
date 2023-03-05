import os
import datetime
from fastapi import APIRouter, security, status
from fastapi.exceptions import HTTPException
from fastapi.params import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from sqlalchemy import exc
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from starlette.requests import Request
from base64 import b64decode
from nacl.secret import SecretBox

from app.database.main import get_database
from ...helpers.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decodeRefreshJWT,
    create_recovery_token,
    get_password_hash,
    decodeRecoverJWT,
)
from ...middlewares.auth import JWTBearer, decodeJWT

from ...helpers.mailer import send_recover_mail
from ..users.model import User
from .schema import LoginSchema, MeResponseSchema, LoginUser


load_dotenv()

VAR = os.getenv("ENV")
secret_key = os.getenv("CRYPT_SECRET_KEY")
router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()

# Verifica si esta autenticado
def is_authenticated(auth_token):
    try:
        if decodeJWT(auth_token):
            return get_database
        else:
            return False

    except Exception as err:
        print("Error message {0}".format(err))


# Wrapper para verificador de autentificación
def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
    return is_authenticated(auth.credentials)


# Login
@router.post("/login", response_model=LoginUser)
async def login_user(login_obj: LoginSchema, db: Session = Depends(get_database)):
    try:
        found_user = db.query(User).filter(User.email == login_obj.email).first()

        if not found_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Este correo no está registrado",
            )

        # # Separador de la contraseña encriptada
        # encrypted = login_obj.password.split(":")
        # # Se decofican las 2 partes
        # nonce = b64decode(encrypted[0])
        # encrypted = b64decode(encrypted[1])
        # # Se convierte la llave secreta en bytes
        # box = SecretBox(bytes(secret_key, encoding="utf8"))
        # # Se desencripta la contraseña
        # decrypted = box.decrypt(encrypted, nonce).decode("utf-8")

        # Verifica si las contraseñas coinciden
        # match_password = verify_password(decrypted, found_user.password)
        match_password = verify_password(login_obj.password, found_user.password)
        if not match_password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Contraseña incorrecta"
            )

        user_obj = {
            "accessToken": create_access_token(found_user.id),
            "refreshToken": create_refresh_token(found_user.id),
            "user": found_user,
        }

        return user_obj
    except exc.SQLAlchemyError as err:
        raise HTTPException(404, format(err))


# Verifica usuario
@router.get("/me", response_model=MeResponseSchema, dependencies=[Depends(JWTBearer())])
async def get_logged_user(request: Request, db: Session = Depends(get_database)):
    try:
        user_id = int(request.user_id)

        current_user = db.query(User).filter(User.id == user_id).first()

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Usuario sin autorización"
            )
        return current_user

    except Exception as err:
        print("Error message : {0}".format(err))
        if hasattr(err, "detail"):
            raise HTTPException(err.status_code, format(err.detail))
        else:
            raise HTTPException(404, format(err))


# Cambio de contraseña
@router.patch("/changepassword")
async def change_password(
    id: int, old_pass: str, new_pass: str, db: Session = Depends(get_database)
):
    try:
        user = db.query(User).filter(User.state == "ACTIVE", User.id == id).first()

        if not user:
            raise HTTPException(
                detail="No existe un usuario con este id:%s" % format(id),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        # Verifica que la contraseña actual coincida con la ingresada
        match_password = verify_password(old_pass, user.password)

        if not match_password:
            raise HTTPException(
                detail="Contraseña antigua erronea",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if old_pass == new_pass:
            raise HTTPException(
                detail="Contraseñas no pueden ser iguales",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        setattr(user, "password", get_password_hash(new_pass))

        db.add(user)
        db.commit()
        db.flush(user)

        return JSONResponse(
            status_code=200,
            content={"message": "USER_UPDATED"},
        )

    except Exception as err:
        print("Error message : {0}".format(err))
        if hasattr(err, "detail"):
            raise HTTPException(404, format(err.detail))
        else:
            raise HTTPException(404, format(err))


# Cambio de token
@router.post("/changetoken", dependencies=[Depends(JWTBearer())])
async def change_token(request: Request, refresh_token: str):
    try:
        token = decodeRefreshJWT(refresh_token)
        user_id = request.user_id

        if not token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Usuarios no coinciden"
            )

        if token["sub"] == user_id:
            access_token = create_access_token(token["sub"])
            return access_token

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Usuario sin autorización"
        )
    except Exception as err:
        print("Error message : {0}".format(err))
        if hasattr(err, "detail"):
            raise HTTPException(404, format(err.detail))
        else:
            raise HTTPException(404, format(err))


# Recuperación de contraseña
@router.post("/forgotpassword")
async def recover_password(email: str, db: Session = Depends(get_database)):
    try:
        found_user = (
            db.query(User).filter(User.email == email, User.state == "ACTIVE").first()
        )
        if not found_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Este correo no está registrado",
            )

        # Se genera token para la recuperación
        recovery_token = create_recovery_token(found_user.id)

        # Envio de correo
        await send_recover_mail(found_user.email, found_user.name, recovery_token)

        return JSONResponse(
            status_code=200,
            content={"message": "EMAIL_SENT"},
        )

    except Exception as err:
        print("Error message : {0}".format(err))
        if hasattr(err, "detail"):
            raise HTTPException(404, format(err.detail))
        else:
            raise HTTPException(404, format(err))


# Cambio de contraseña al recuperar
@router.post("/recoverpassword")
async def recovery_password(
    recover_token: str, new_pass: str, db: Session = Depends(get_database)
):
    try:
        # Se decodifica el token de recuperación
        token = decodeRecoverJWT(recover_token)

        if not token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token Inválido"
            )

        user = (
            db.query(User)
            .filter(User.state == "ACTIVE", User.id == token["sub"])
            .first()
        )

        setattr(user, "password", get_password_hash(new_pass))

        db.add(user)
        db.commit()
        db.flush(user)

        return JSONResponse(
            status_code=200,
            content={"message": "USER_UPDATED"},
        )

    except Exception as err:
        print("Error message : {0}".format(err))
        if hasattr(err, "detail"):
            raise HTTPException(404, format(err.detail))
        else:
            raise HTTPException(404, format(err))
