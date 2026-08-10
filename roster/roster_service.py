from storage.fake_db import FakeDB
from roster.roster_cache import RosterCache

class RosterService:
    def __init__(self, cache):
        self.cache = RosterCache()

    def get_agents(self):
        return self.cache.agents.values()
    
    def refresh_cache(self):
        """
        Refresh the roster cache with the latest agent data
        """
        fake_db = FakeDB()
        agents = fake_db.get_agents_from_db() ## replace with actual database call
        self.cache.update(agents)



