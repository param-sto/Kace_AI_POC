from clients.graph_client import GraphClient
from config import settings
from datetime import datetime
from models.agent import Agent

def get_agents_from_sharepoint() -> list[Agent]:
    graph_client = GraphClient(
                client_id=settings.client_id,
                client_secret=settings.client_secret,
                tenant_id=settings.tenant_id,
                graph_scope=settings.graph_scope,
                shared_mailbox=settings.shared_mailbox
                )
    graph_client.authenticate()
    data = graph_client.get_sharepoint_roster(settings.kace_base_url, settings.sharepoint_site_id, settings.sharepoint_list_id)
    agents = []
    for item in data: 
        fields = item["fields"]
        agent = Agent(
                name = fields["Title"],
                routing_order = int(fields["routing_order"]),
                unique_id = int(fields["unique_id"]),
                start_time = datetime.strptime(fields["start_time"], "%H:%M").time(),
                end_time = datetime.strptime(fields["end_time"], "%H:%M").time(),
                active = fields["active"] == "True",
                on_vacation = fields["on_vacation"] == "True"
                )
        agents.append(agent)
    return agents