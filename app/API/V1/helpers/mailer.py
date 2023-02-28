from fastapi import FastAPI

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


from app.settings import USER_NAME, PASSWORD, MAIL_FROM, MAIL_SERVER, MAIL_PORT, ENV

# Configuración del envío de correos
conf = ConnectionConfig(
    MAIL_USERNAME=USER_NAME,
    MAIL_PASSWORD=PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM_NAME="Sergio Escalona",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS =False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER="app/API/v1/templates",
)

app = FastAPI()


# Correo de recuperación de contraseña
async def send_recover_mail(email: str, name: str, token: str):

    if ENV == "development":
        link = "http://localhost:3000/cambio_password/"
    else:
        link = "https://www.website.cl/cambio_password/"
    message = MessageSchema(
        subject="Cambio de contraseña",
        recipients=[email],
        template_body={
            "link": link + token,
            "userName": name,
        },
        subtype="html",
    )

    fm = FastMail(conf)
    if await fm.send_message(message, template_name="passRecover.html"):
        return True
    return False


# Correo de bienvenida
async def send_welcome_mail(email: str, name: str, password: str):

    if ENV == "development":
        link = "http://localhost:3000/login/"
    else:
        link = "https://www.website.cl/login/"
    message = MessageSchema(
        subject="Bienvenido al portal Serfusan",
        recipients=[email],
        template_body={
            "link": link,
            "userName": name,
            "email": email,
            "password": password,
        },
        subtype="html",
    )

    fm = FastMail(conf)
    if await fm.send_message(message, template_name="welcome.html"):
        return True
    return False
