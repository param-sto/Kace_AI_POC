from clients.graph_client import GraphClient
from config import settings
from cleaner import emailCleaner

def extract_information_from_email(message_id: str):
    graph_client = GraphClient(
        client_id=settings.client_id,
        client_secret=settings.client_secret,
        tenant_id=settings.tenant_id,
        graph_scope=settings.graph_scope,
        shared_mailbox=settings.shared_mailbox
    )
    graph_client.authenticate()
    content = graph_client.get_message(message_id)
    cleaner = emailCleaner()
    email = {"id":content["id"], 
            "subject":content["subject"], 
            "from":content["from"]["emailAddress"]["address"], 
            "body":content["body"]["content"], 
            "conversationId":content["conversationId"], 
            "receivedDateTime":content["receivedDateTime"],
            "name":content["from"]["emailAddress"]["name"]
            }
    email["body"] = cleaner.clean_email(email["body"], content["body"]["contentType"], email["name"])
    return email