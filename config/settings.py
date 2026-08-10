import os
from dotenv import load_dotenv
load_dotenv()
tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
shared_mailbox = os.getenv("SHARED_MAILBOX")
graph_scope = os.getenv("GRAPH_SCOPE")
backend_url = os.getenv("BACKEND_URL")
azure_sql_connectionstring = os.getenv("AZURE_SQL_CONNECTIONSTRING")
azure_queue_connection_string = os.getenv("AZURE_QUEUE_CONNECTION_STRING")
azure_queue_name = os.getenv("AZURE_QUEUE_NAME")

