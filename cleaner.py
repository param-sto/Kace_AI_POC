import re
from bs4 import BeautifulSoup
from models.agent import Agent
from datetime import datetime

class emailCleaner:
    def clean_email(self, email_body: str, content_type: str, name: str) -> str:
        """
        Clean the email body by removing HTML tags and extra whitespace.
        """
        if content_type == "html":
            soup = BeautifulSoup(email_body, "html.parser")
            body = soup.get_text("\n").strip()
            signature_markers = [
            "\nRegards,",
            "\nThanks,",
            "\nBest",
            "\nSincerely",
            "\nFrom"
            ]
            for marker in signature_markers:
                if marker.lower() in body.lower():
                    index = body.lower().find(marker.lower())
                    body = body[:index]
            body = re.sub(r"\n,\s*\n+", "\n", body)
            body = re.sub(r"\xa0", " ", body).strip()
            if name in body:
                idx = body.find(name)
                body = body[:idx]
            return body.strip()
        return email_body.strip()

    def clean_sharepoint_data(self, data):
        agents= []
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
    