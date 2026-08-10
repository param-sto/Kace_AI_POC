import json
from azure.storage.queue import QueueClient
from config import settings

class QueueStorageClient:
    def __init__(self):
        self.queue_client = QueueClient.from_connection_string(
            conn_str=settings.azure_queue_connection_string, 
            queue_name=settings.azure_queue_name
        )

    def send_message(self, message_id:str):
        """
        Adds message to queue
        """
        message = {"message_id": message_id}

        self.queue_client.send_message(json.dumps(message))