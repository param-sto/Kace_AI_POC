from datetime import datetime, timedelta, timezone
import requests
from clients.graph_client import GraphClient
from config import settings

class SubscriptionManager:
    def __init__(self):
        self.graph = GraphClient(
            client_id=settings.client_id,
            client_secret=settings.client_secret,
            tenant_id=settings.tenant_id,
            graph_scope=settings.graph_scope,
            shared_mailbox=settings.shared_mailbox
        )
        self.graph.authenticate()
    
    def create_subscription(self):
        expiration = (datetime.now(timezone.utc)
        + timedelta(hours=1)).isoformat()

        body = {
            "changeType": "created",
            "notificationUrl": f"{settings.backend_url}", 
            "resource": f"users/{settings.shared_mailbox}/messages",
            "expirationDateTime": expiration ,
            "clientState": "secret"
        }
        response = requests.post(
            "https://graph.microsoft.com/v1.0/subscriptions",
            headers=self.graph.get_header(),
            json=body
        )
        if response.status_code == 201:
            print("Subscription created successfully.")
            subscription = response.json()
            self.subscription_id = subscription["id"]
            return subscription
        else:
            print(f"Failed to create subscription: {response.text}")
            return None
    
    def renew_subscription(self, subscription_id: str):
        expiration = (datetime.now(timezone.utc)
        + timedelta(hours=1)).isoformat()

        body = {
            "expirationDateTime": expiration
            }
        response = requests.patch(
            f"https://graph.microsoft.com/v1.0/subscriptions/{subscription_id}",
            headers=self.graph.get_header(),
            json=body
        )
        if response.status_code == 200:
            print("Subscription renewed successfully.")
            return response.json()
        else:
            print(f"Failed to renew subscription: {response.text}")
            return None

#.\.venv\Scripts\Activate.ps1