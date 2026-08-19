from fastapi import FastAPI
from ingestion.webhook_receiver import router 
from contextlib import asynccontextmanager
from roster.roster_cache import RosterCache
from roster.roster_service import RosterService
from workers.sql_worker import SQLWorker
from assignment.availability_service import AvailabilityService
from assignment.routing_service import RoutingService
from clients.sql_client import SQLClient
from workers.email_worker import EmailWorker
from clients.queue_client import QueueStorageClient
from clients.graph_client import GraphClient
from config import settings 
from ticketing.ticket_service import TicketService
from clients.kace_client import KaceClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    roster_cache = RosterCache()
    roster_service = RosterService(roster_cache)
    roster_service.refresh_cache(settings.sharepoint_site_url_base, settings.sharepoint_site_id, settings.sharepoint_list_id)
    availability_service = AvailabilityService()
    sql_client = SQLClient()
    sql_worker = SQLWorker(sql_client)
    routing_service = RoutingService(roster_service, availability_service, sql_worker)
    queue_client = QueueStorageClient()
    kace_client = KaceClient(settings.kace_base_url, settings.kace_username, settings.kace_password)
    result = kace_client.authenticate_kace()
    ticket_service = TicketService(kace_client)
    email_worker = EmailWorker(queue_client, sql_worker, routing_service, ticket_service)
    graph_client = GraphClient(
                    client_id=settings.client_id,
                    client_secret=settings.client_secret,
                    tenant_id=settings.tenant_id,
                    graph_scope=settings.graph_scope,
                    shared_mailbox=settings.shared_mailbox
                    )
    app.state.email_worker = email_worker
    app.state.queue_client = queue_client
    yield 

app = FastAPI(lifespan=lifespan)



app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "running"}
