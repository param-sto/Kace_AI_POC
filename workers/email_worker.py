from ingestion.email_reader import extract_information_from_email
import time
from workers.sql_worker import SQLWorker

class EmailWorker:

    def __init__(self, queue_client, sql_worker, routing_service, ticketing_service):
        self.queue_client = queue_client
        self.sql_worker = sql_worker
        self.routing_service = routing_service
        self.ticketing_service = ticketing_service

    def process_emails(self):
        message = self.queue_client.get_message()
        if message is None:
            return 
        print("=" * 50)
        message_id = message["message_id"]
        deletion_id = message["deletion_id"]
        unique_id = message["unique_id"]
        email = extract_information_from_email(message_id)
        conv_id = email["conversationId"]
        body = email["body"]
        answer = self.sql_worker.get_conversation_info(conv_id)
        if answer == None:
            agent = self.routing_service.get_next_available_agent()
            if agent is None:
                raise RuntimeError("No agent is available right now")
            data = self.convert_email_to_ticket(email, agent)
            response = self.ticketing_service.create_ticket(data)
            ticket_id = response["IDs"][0]
            self.ticketing_service.append_comment(3, ticket_id, body)
            self.sql_worker.create_conversation(conv_id, agent.unique_id, ticket_id)
            self.queue_client.delete_message(unique_id, deletion_id)
        else:
            ticket_id = answer["ticket_id"]
            self.ticketing_service.append_comment(3, ticket_id, body)
            self.queue_client.delete_message(unique_id, deletion_id)

    def convert_email_to_ticket(self, email, agent):
        """
        Convert the email object to a ticket object, mapping out the fields. 
        """
        ticket_fields = {
                "Tickets": [{
                    "hd_queue_id": 3,
                    "title": None,
                    "summary": None,
                    "owner": None,
                    "cc_list": None,
                    "custom_16": None,
                    "owner": {"id": None}
                    }]
            }
        

        ticket_fields["Tickets"][0]["title"] = email["subject"]
        ticket_fields["Tickets"][0]["summary"] = email["body"]
        ticket_fields["Tickets"][0]["cc_list"] = email["from"]
        ticket_fields["Tickets"][0]["owner"]["id"] = agent.unique_id
        ticket_fields["Tickets"][0]["custom_16"] = email["from"]


        return ticket_fields


    


        




