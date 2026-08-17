from models.agent import Agent
from datetime import time

class RosterCache:
    def __init__(self):
        self.agents = {}

    def update(self, agents_list: list[Agent]):
        """
        Load agents into the roster cache from a list of Agent objects
        """
        for agent in agents_list:
            self.agents[agent.routing_order] = agent
