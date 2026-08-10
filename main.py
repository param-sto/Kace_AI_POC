from fastapi import FastAPI
from ingestion.webhook_receiver import router 

app = FastAPI()

app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "running"}
