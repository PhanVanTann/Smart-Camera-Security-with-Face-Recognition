from fastapi import FastAPI
from app.api.residents import router as residents_router

app = FastAPI(title="Smart Security Camera")

app.include_router(residents_router)


@app.get("/")
def root():
    return {"message": "Smart Security Camera API is running"}


@app.get("/health")
def health():
    return {"status": "OK"}