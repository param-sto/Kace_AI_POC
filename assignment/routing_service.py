from roster.roster_service import RosterService
from assignment.round_robin import RoundRobin
from assignment.availability_service import AvailabilityService
from storage.fake_db import FakeDB

def get_next_available_agent():
    # Get a list of all agents from the roster service
    agents = []
    roster_service = RosterService(agents)
    roster_service.refresh_cache()
    agents = roster_service.get_agents()

    # Filter the agents to only include those who are available
    availability_service = AvailabilityService()
    available_agents = availability_service.get_available_agents(agents)

    # Create a round-robin instance
    fake_database = FakeDB()
    round_robin = RoundRobin(fake_database)
    next_agent = round_robin.get_next_agent(available_agents)
    return next_agent

print(get_next_available_agent())
print(get_next_available_agent())
print(get_next_available_agent())