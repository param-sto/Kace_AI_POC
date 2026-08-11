import json
from azure.storage.queue import QueueClient
from config import settings

class QueueStorageClient:
    def __init__(self, message_id:str):
        self.queue_client = QueueClient.from_connection_string(
            conn_str=settings.azure_queue_connection_string, 
            queue_name=settings.azure_queue_name
        )
        self.message_id = message_id

    def send_message(self):
        """
        Adds message to queue
        """
        message = {"message_id": self.message_id}

        self.queue_client.send_message(json.dumps(message))

    def get_message(self):
        """
        Reads message from queue
        """
        message = self.queue_client.receive_message()
        payload = json.loads(message.content)
        extracted = {
            "unique_id": message.id,
            "read_count": message.dequeue_count,
            "message_id": payload["message_id"],
            "deletion_id": message.pop_receipt
        }

        return extracted

    def delete_message(self, unique_id:str, deletion_id:str):
        """
        Deletes message from queue upon successful processing
        """
        self,self.queue_client.delete_message(unique_id, deletion_id)

    def get_queue_depth(self):
        properties = self.queue_client.get_queue_properties()
        count = properties.approximate_message_count
        print(count)
