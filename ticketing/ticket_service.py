from config import settings
import requests
class TicketService:

    def __init__(self, kace_client):
        self.client = kace_client

    def get_queues(self):
        return self.client.get("/api/service_desk/queues")

    def get_queue_fields(self, queue_id: int):
        return self.client.get(f"/api/service_desk/queues/{queue_id}/fields")

    def create_ticket(self, ticket_data: dict):
        return self.client.post("/api/service_desk/tickets", ticket_data)

    def append_to_ticket(self, ticket_id: int, message: str):
        """
        Append a message to an existing KACE coversation.
        """
        payload = {
            "Work": [
                {
                    "note": message
                }
            ]
        }
        return self.client.post(f"/api/service_desk/tickets/{ticket_id}/work", payload)

    def append_comment(self, queue_id: int, ticket_id: int, comment: str, owners_only: bool = False):

        csrf_token = self.client.get_admin_csrf_token()

        files = {
            "QUEUE_ID": (None, str(queue_id)),
            "TICKET_ID": (None, str(ticket_id)),
            "UPDATE_TYPE": (None, "add_comment"),
            "COMMENT": (None, comment),
            "SCREENSHOT_DATA": (None, ""),
            "OWNERS_ONLY": (
                None,
                "1" if owners_only else "0"
            ),
            "CSRF_TOKEN": (None, csrf_token)
        }

        response = self.client.session.post(
            f"{self.client.base_url}/common/ajax_update_ticket.php",
            files=files,
            verify=False,
            headers={
                "X-Requested-With": "XMLHttpRequest"
            }
        )

        response.raise_for_status()
        if response.text.strip():
            try:
                return response.json()
            except ValueError:
                return response.text
        return {"success": True}