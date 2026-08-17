from ingestion.email_reader import extract_information_from_email
import time
from workers.sql_worker import SQLWorker

class EmailWorker:

    def __init__(self, queue_client, sql_worker, routing_service):
        self.queue_client = queue_client
        self.sql_worker = sql_worker
        self.routing_service = routing_service

    def process_emails(self):
        message = self.queue_client.get_message()
        print("message taken from queue")
        if message is None:
            time.sleep(5)
        message_id = message["message_id"]
        deletion_id = message["deletion_id"]
        unique_id = message["unique_id"]
        print("extracting info...")
        print(message_id)
        email = extract_information_from_email(message_id)
        conv_id = email["conversationId"]
        print("ckecking if conv alrerdy exists,....")
        answer = self.sql_worker.get_conversation_agent(conv_id)
        if answer == None:
            print("creating ticket")
            agent = self.routing_service.get_next_available_agent()
            self.sql_worker.create_conversation(conv_id, agent.unique_id)
            self.queue_client.delete_message(unique_id, deletion_id)
            print(agent)
            print(email)
        else:
            self.queue_client.delete_message(unique_id, deletion_id)
            print("appending ticket")
            print(answer)
            print(email)

        




