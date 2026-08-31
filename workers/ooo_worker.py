from datetime import datetime
from zoneinfo import ZoneInfo

class OOOWorker:
    def __init__(self, graph_client):
        self.graph_client = graph_client

    def is_out_of_office(self, user_email: str) -> bool:
        """
        Returns True if the user is currently out of office.
        """
        settings = self.graph_client.get_auto_reply_settings(user_email)

        status = settings["status"]

        # OOO is permanently enabled
        if status == "alwaysEnabled":
            return True

        # OOO is disabled
        if status == "disabled":
            return False

        # OOO is scheduled
        if status == "scheduled":

            start = settings["scheduledStartDateTime"]
            end = settings["scheduledEndDateTime"]

            start_time = self._convert_graph_time(start)
            end_time = self._convert_graph_time(end)

            now = datetime.now(start_time.tzinfo)

            return start_time <= now <= end_time

        return False

    def _convert_graph_time(self, graph_time):
        """
        Converts a Microsoft Graph dateTimeTimeZone object
        into a timezone-aware Python datetime.
        """

        date_time = graph_time["dateTime"]
        time_zone = graph_time["timeZone"]

        # Microsoft Graph may return Windows timezone names.
        windows_to_iana = {
            "Eastern Standard Time": "America/Toronto",
            "Central Standard Time": "America/Winnipeg",
            "Mountain Standard Time": "America/Edmonton",
            "Pacific Standard Time": "America/Vancouver",
        }

        iana_zone = windows_to_iana.get(
            time_zone,
            "America/Toronto"
        )

        return datetime.fromisoformat(
            date_time
        ).replace(
            tzinfo=ZoneInfo(iana_zone)
        )