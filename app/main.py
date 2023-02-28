from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.API.V1 import router as V1_Routes
from app.database.main import get_database


app = FastAPI(
    tittle='Proyecto',
    description='Proyecto',
    version='1.0.0')

app.include_router(V1_Routes.router, prefix="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["Main"])
async def main():
    return {"message": "PROYECTO API"}


@app.on_event("startup")
async def startup():
    get_database()
