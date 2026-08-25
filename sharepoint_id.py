import requests
from clients.graph_client import GraphClient
from config import settings
from models.agent import Agent
from roster.roster_service import RosterService
from roster.roster_cache import RosterCache
from workers.ooo_worker import OOOWorker


tenant_id = settings.tenant_id
client_id = settings.client_id
client_secret = settings.client_secret
graph_scope = settings.graph_scope
shared_mailbox = settings.shared_mailbox
base_url = settings.sharepoint_site_url_base
site_id = settings.sharepoint_site_id
list_id = settings.sharepoint_list_id

graph_client = GraphClient(client_id, client_secret, tenant_id, graph_scope, shared_mailbox)
ooo_worker = OOOWorker(graph_client)
result = ooo_worker.is_out_of_office(shared_mailbox)
print(result)
# graph_client.authenticate()
# agents = graph_client.get_sharepoint_roster(base_url, site_id, list_id)
# print(agents)
# response = requests.get(
#     site_url, headers=graph_client.get_header()
# )
# response.raise_for_status()

# site = response.json()
# id = site["value"]
# print(id)
# agents = []
# items = graph_client.get_sharepoint_list_items(base_url, site_id, list_id)
# for item in items: 
#     fields = item["fields"]
#     agent = Agent(
#         name = fields["Title"],
#         routing_order = int(fields["routing_order"]),
#         unique_id = int(fields["unique_id"]),
#         start_time = fields["start_time"],
#         end_time = fields["end_time"],
#         active = fields["active"] == "True",
#         on_vacation = fields["on_vacation"] == "True"
#     )
#     agents.append(agent)

# print(agents)
# roster_cache = RosterCache()
# roster_service = RosterService(roster_cache)
# roster_service.refresh_cache(base_url, site_id, list_id)
# agents = roster_service.get_agents()
# print(agents)



