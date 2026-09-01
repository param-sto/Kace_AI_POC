from clients.graph_client import GraphClient
from roster.roster_cache import RosterCache
from config import settings

class RosterService:
    def __init__(self, cache, sharepoint_worker):
        self.cache = cache
        self.sharepoint_worker = sharepoint_worker

    def get_agents(self):
        return self.cache.agents
    
    def refresh_cache(self, base_url: str, site_id: str, list_id: str):
        """
        Refresh the roster cache with the latest agent data
        """
        agents = self.sharepoint_worker.get_agents_from_sharepoint()
        self.cache.update(agents)



