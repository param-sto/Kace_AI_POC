from datetime import datetime

class AvailabilityService:
    def get_available_agents(self, agents):
        now = datetime.now().time()
        availible_agents = []
        for agent in agents:
            if agent.on_vacation or not agent.active:
                continue
            if not(agent.shift_start <= now <= agent.shift_end):
                continue
            availible_agents.append(agent)
        return availible_agents