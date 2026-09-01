from msal import ConfidentialClientApplication
import requests
from cleaner import emailCleaner


class GraphClient:
    def __init__(self, client_id, client_secret, tenant_id, graph_scope, shared_mailbox):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.graph_scope = graph_scope
        self.shared_mailbox = shared_mailbox

    def authenticate(self):
        """
        Authenticate with Microsoft Entra ID and return the access token.
        """
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"

        app = ConfidentialClientApplication(
            client_id=self.client_id,
            authority=authority,
            client_credential=self.client_secret
        )

        result = app.acquire_token_for_client(
            scopes=[self.graph_scope]
        )

        if "access_token" in result:
            self.access_token = result["access_token"]
            return result["access_token"]

        raise Exception(
            result.get("error_description", "Failed to authenticate"
            )
        )

    def get_header(self):
        """
        Gets the autorization header for Microsoft Graph API
        """
        return {"Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
        }
    def get_message(self, message_id: str):
        """
        Get messages from the shared mailboxgiven the Message ID.
        """
        url = (
            f"https://graph.microsoft.com/v1.0"
            f"/users/{self.shared_mailbox}/mailFolders('inbox')/messages/{message_id}"
            f"?$select=subject,from,body,conversationId,receivedDateTime"
        )
        response = requests.get(url, headers=self.get_header())
        if response.status_code == 200:
            email = response.json()
            return email   
        else:
            raise Exception("Failed to get message:", response.text )

    def get_sharepoint_roster(self, base_url: str, site_id: str, list_id: str):
        """
        Retrieves all items from a sharepoint list.
        """
        url = (
        f"{base_url}/{site_id}/lists/{list_id}/items?expand=fields"
        "($select=Title,unique_id,start_time,end_time,active,on_vacation,routing_order)"
            )

        response = requests.get(
            url, 
            headers=self.get_header()
        )

        data = response.json()["value"]
        return data

    def get_auto_reply_settings(self, user_email: str):
        """
        Gets the automatic reply settings for a user.
        """
        url = (
            f"https://graph.microsoft.com/v1.0/"
            f"users/{user_email}/mailboxSettings/"
            f"automaticRepliesSetting"
        )
        self.authenticate()
        response = requests.get(url, headers=self.get_header())
        response.raise_for_status()
        return response.json()
        