from clients.graph_client import GraphClient
from roster.roster_cache import RosterCache
from config import settings

class RosterService:
    def __init__(self, cache):
        self.cache = RosterCache()

    def get_agents(self):
        return self.cache.agents
    
    def refresh_cache(self, base_url: str, site_id: str, list_id: str):
        """
        Refresh the roster cache with the latest agent data
        """
        graph_client = GraphClient(
                        client_id=settings.client_id,
                        client_secret=settings.client_secret,
                        tenant_id=settings.tenant_id,
                        graph_scope=settings.graph_scope,
                        shared_mailbox=settings.shared_mailbox
                        )
        graph_client.authenticate()
        agents = graph_client.get_sharepoint_roster(settings.sharepoint_site_url_base, settings.sharepoint_site_id, settings.sharepoint_list_id)
        self.cache.update(agents)



