from clients.graph_client import GraphClient
from config import settings
from datetime import datetime
from models.agent import Agent

class SharepointWorker:
    def __init__(self, graph_client):
        self.graph_client = graph_client
    def get_agents_from_sharepoint(self) -> list[Agent]:
        """
        Gets updated agent roster from SharePoint List.
        """
        data = self.graph_client.get_sharepoint_roster(settings.sharepoint_site_url_base, settings.sharepoint_site_id, settings.sharepoint_list_id)
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