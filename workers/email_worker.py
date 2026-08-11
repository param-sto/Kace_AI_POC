from ingestion.email_reader import extract_information_from_email
from assignment.routing_service import get_next_available_agent
import time

class EmailWorker:

    def __init__(self, queue_client):
        self.queue_client = queue_client

    def process_emails(self):
        message = self.queue_client.get_message()
        print("message taken from queue")
        if message is None:
            time.sleep(5)
        message_id = message["message_id"]
        print("extracting info...")
        print(message_id)
        email = extract_information_from_email(message_id)
        print("getting angent")
        agent = get_next_available_agent()
        print(email)
        print(agent)
        




