from fastapi import FastAPI
from .routes import router

app = FastAPI(title="API Pessoas - psycopg")


app.include_router(router)