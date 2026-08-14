import os
from dotenv import load_dotenv
load_dotenv()
tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
shared_mailbox = os.getenv("SHARED_MAILBOX")
graph_scope = os.getenv("GRAPH_SCOPE")
backend_url = os.getenv("BACKEND_URL")
azure_sql_connection_string = os.getenv("AZURE_SQL_CONNECTION_STRING")
azure_queue_connection_string = os.getenv("AZURE_QUEUE_CONNECTION_STRING")
azure_queue_name = os.getenv("AZURE_QUEUE_NAME")
sharepoint_site_url_base = os.getenv("SHAREPOINT_SITE_URL_BASE")
sharepoint_hostname = os.getenv("SHAREPOINT_HOSTNAME")
sharepoint_site_path = os.getenv("SHAREPOINT_SITE_PATH")
sharepoint_site_id = os.getenv("SHAREPOINT_SITE_ID")
sharepoint_list_id = os.getenv("SHAREPOINT_LIST_ID")
kace_username = os.getenv("KACE_USERNAME")
kace_password = os.getenv("KACE_PASSWORD")
kace_base_url = os.getenv("KACE_BASE_URL")


