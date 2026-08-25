from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from clients.queue_client import QueueStorageClient
from workers.email_worker import EmailWorker
from workers.sql_worker import SQLWorker
from clients.sql_client import SQLClient

router = APIRouter()
class  GraphNotification(BaseModel):
    value: list

@router.get("/webhook")
async def validate_webhook(validationToken: str | None = None):
    """
    Validate the webhook subscription with Microsoft graph witin the 10 seconds window.
    """
    if validationToken:
        return PlainTextResponse(validationToken)
    return PlainTextResponse("OK")

@router.post("/webhook")
async def receive_notification(request: Request):
    """
    Endpoint to receive webhook notifications from Microsoft Graph.
    """
    validation_token = request.query_params.get("validationToken")
    if validation_token:
        return PlainTextResponse(validation_token)

    body = await request.json()
    message_id = body["value"][0]["resourceData"]["id"]
    queue_client = request.app.state.queue_client
    queue_client.send_message(message_id)
    email_worker = request.app.state.email_worker
    email_worker.process_emails()

    return{"status": "received"}

# http://127.0.0.1:8000/docs