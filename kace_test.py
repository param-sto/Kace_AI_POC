from clients.kace_client import KaceClient
from config import settings
from ticketing.ticket_service import TicketService

data = {
    "Tickets": [{
    "hd_queue_id": 3, 
    "title": "Test",
    "summary": "This is a test ticket",
    "custom_16": "param.khurana@skilledtradesontario.ca"
}]
}
kace_client = KaceClient(
    settings.kace_base_url,
    settings.kace_username,
    settings.kace_password
)

result = kace_client.authenticate_kace()
print("Authentication Successful")

ticket_service = TicketService(kace_client)
# queues = ticket_service.get_queues()
# print(queues)
fields = ticket_service.get_queue_fields(3)
print(fields)
# response = ticket_service.create_ticket(data)
# print(response)
# me = kace_client.get("/api/users/me/")
# print(me)