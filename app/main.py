from fastapi import FastAPI

app = FastAPI(title="Smart Security Camera")

@app.get("/")
def root():
    return {"message": "Smart Security Camera API is running"}

@app.get("/health")
def health():
    return {"status": "OK"}