from clients.graph_client import GraphClient
from config import settings
from cleaner import emailCleaner
from ingestion.subscription_manager import SubscriptionManager
from ingestion.email_reader import extract_information_from_email
from roster.roster_service import RosterService
from models.agent import Agent
from clients.sql_client import SQLClient
from clients.queue_client import QueueStorageClient

subscription_manager = SubscriptionManager()
print(subscription_manager.create_subscription())



#response = extract_information_from_email("AAMkAGUzMDNhMDc5LTQ2MWEtNDNhMy04MTUxLTU5YzI4YzM1ZWI4NABGAAAAAAAV61gj875eTZ1LEpERW2CABwCjakla1gmRRZRgYj71UrpVAAAAAAEMAACjakla1gmRRZRgYj71UrpVAAATWvN9AAA=")
#print(response)
#cleaner = emailCleaner()
# email = {"id":response["value"][0]["id"], 
#         "subject":response["value"][0]["subject"], 
#         "from":response["value"][0]["from"]["emailAddress"]["address"], 
#         "body":cleaner.clean_email(response["value"][0]["body"]["content"], response["value"][0]["body"]["contentType"]), 
#         "conversationId":response["value"][0]["conversationId"], 
#         "receivedDateTime":response["value"][0]["receivedDateTime"]
#         }

# database = FakeDB()
# roster = RosterService(database)
# agents = roster.

# for agent in agents:
#     print (agent.name)

# print(settings.azure_sql_connectionstring)

# sql_client = SQLClient()
# num = sql_client.test_connection()
# print(num)
# msg_id = "abcd1234rufiyfj=hou6bv8"
queue_client = QueueStorageClient()
queue_client.clear_queue()
# queue_client.send_message()
# msg = queue_client.get_message()
# print(msg)
# queue_client.get_queue_depth()
# id = msg["unique_id"]
# deletion_id = msg["deletion_id"]
# queue_client.delete_message(id, deletion_id)
# queue_client.get_queue_depth()


