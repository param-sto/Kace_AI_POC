
class TicketService:

    def __init__(self, kace_client):
        self.client = kace_client

    def get_queues(self):
        return self.client.get("/api/service_desk/queues")

    def get_queue_fields(self, queue_id: int):
        return self.client.get(f"/api/service_desk/queues/{queue_id}/fields")

    def create_ticket(self, ticket_data: dict):
        return self.client.post("/api/service_desk/tickets", ticket_data)