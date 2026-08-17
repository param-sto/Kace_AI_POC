from assignment.routing_service import RoutingService
from roster.roster_service import RosterService
from workers.sql_worker import SQLWorker
from roster.roster_cache import RosterCache
from clients.sql_client import SQLClient
from assignment.availability_service import AvailabilityService
from config import settings
roster_cache = RosterCache()
roster_service = RosterService(roster_cache)
availability_service = AvailabilityService()
sql_client = SQLClient()
sql_worker = SQLWorker(sql_client)
routing_service = RoutingService(roster_service, availability_service, sql_worker)
roster_service.refresh_cache(settings.sharepoint_site_url_base, settings.sharepoint_site_id, settings.sharepoint_list_id)
agent = routing_service.get_next_available_agent()
print(roster_service.get_agents())
print(agent)