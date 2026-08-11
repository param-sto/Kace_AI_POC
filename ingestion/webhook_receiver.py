from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from clients.queue_client import QueueStorageClient
from workers.email_worker import EmailWorker

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
    print(message_id)
    queue_client = QueueStorageClient(message_id)
    queue_client.send_message()
    email_worker = EmailWorker(queue_client)
    email_worker.process_emails()

# http://127.0.0.1:8000/docs