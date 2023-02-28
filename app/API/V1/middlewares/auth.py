from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..helpers.security import decodeJWT

# Verificación de token
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Formato de token inválid")
            validation = self.verify_jwt(credentials.credentials)
            if not validation["isTokenValid"]:
                raise HTTPException(status_code=403, detail="Token inválido o expirado")
            request.user_id = validation["user_id"]
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Authorización inválida")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None

        if payload:
            isTokenValid = True
        return {"isTokenValid": isTokenValid, "user_id": payload["sub"]}
