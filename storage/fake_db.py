from datetime import time
from models.agent import Agent
from models.conversation import Conversation

class FakeDB:
    def __init__(self):
        self.agents = [
            Agent(
                id = 164,
                name = "Alice",
                email = "Alice@test.com",
                shift_start = time(7, 0),
                shift_end = time(15, 0),
                on_vacation = False,
                active = True,
                active_tickets = 5,
                routing_order = 1
            ),
            Agent(
                id = 144,
                name = "Bob",
                email = "bob@test.com",
                shift_start = time(9, 0),
                shift_end = time(18, 0),
                on_vacation = False,
                active = True,
                active_tickets = 3,
                routing_order = 2
            ),
            Agent(
                id = 99,
                name = "Charlie",
                email = "charlie@test.com",
                shift_start = time(11, 0),
                shift_end = time(22, 0),
                on_vacation = False,
                active = True,
                active_tickets = 0,
                routing_order = 3
            )

        ]
        self.conversations = {}
        self.round_robin_idx = 0

    def get_agents_from_db(self):
        """
        Returns a list of all agents in the database
        """
        return self.agents
        
    def get_conversation_owner(self, conversation_id: str) -> str:
        """
        Returns the assigned agent for a given conversation ID 
        """
        return self.conversations.get(conversation_id, None)
        
    def assign_conversation(self, conversation_id: str, agent_name: str):
        """
        Assign conversation to an agent and update the conversation owner in the database
        """
        self.conversations[conversation_id] = agent_name