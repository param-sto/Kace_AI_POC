from roster.roster_service import RosterService
from assignment.round_robin import RoundRobin
from assignment.availability_service import AvailabilityService

class RoutingService:

    def __init__(self, roster_service, availability_service, sql_worker):
        self.roster_service = roster_service
        self.availability_service = availability_service
        self.sql_worker = sql_worker

    def get_next_available_agent(self):
        # Get a dict of all agents from the roster service
        agents = self.roster_service.get_agents()
        start_index = self.sql_worker.get_routing_state("IT")
        for offset in range(len(agents)):
            index = (start_index + offset)%len(agents)
            agent = agents[index]
            if self.availability_service.is_available(agent):
                next_index = (index+1)%len(agents)
                self.sql_worker.update_routing_state("IT", next_index)
                return agent

        return None

    
