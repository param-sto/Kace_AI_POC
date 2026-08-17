
class RoundRobin:
    def __init__(self, db):
        self.db = db

    def get_next_agent(self, agents):
        if not agents:
            return None
        current_index = self.db.get_routing_state("IT") #change with the respective dept
        total_agents = len(agents)
        agent = agents[current_index]

        self.db.update_routing_sate("IT", (current_index + 1) % total_agents)
        return agent
