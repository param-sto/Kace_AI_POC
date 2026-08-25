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
# print("Authentication Successful")
ticket_service = TicketService(kace_client)
# queues = ticket_service.get_queues()
# print(queues)
# fields = ticket_service.get_queue_fields(3)
# print(fields)
# response = ticket_service.create_ticket(data)
# print(response)
# me = kace_client.get("/api/users/me/")
# print(me)
# response = ticket_service.append_to_ticket(58, "this is a test222")
# print(response)

kace_client.authenticate_admin_ui()
ticket_service.append_comment(3, 75, "Appending works!!!!", False)

# csrf_token = kace_client.get_csrf_token()
# print(csrf_token)
# kace_client.authenticate_admin_ui()
# kace_client.get_admin_csrf_token()
