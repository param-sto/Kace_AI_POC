from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from ingestion.email_reader import extract_information_from_email
from assignment.routing_service import get_next_available_agent

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
    email = extract_information_from_email(message_id)
    print(email)
    print("\n")
    agent = get_next_available_agent()
    print(agent)
    return {"status": "received"}
# http://127.0.0.1:8000/docs