from dataclasses import dataclass
from datetime import datetime

@dataclass
class Email:

    message_id:str
    subject:str
    sender:str
    sender_name:str

    body:str
    received_datetime: datetime
    conversation_id:str