from dataclasses import dataclass

@dataclass
class Conversation:
    conversation_id:str
    assigned_agent:str
    status:str