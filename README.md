# KACE AI POC

Proof of concept for automating shared mailbox email processing and KACE ticket management.

The application receives email notifications through Microsoft Graph webhooks, queues them in Azure Queue Storage, processes them in the background, tracks conversations in Azure SQL, routes new conversations to available agents, and creates or updates KACE tickets.

## Architecture

```text
Microsoft Graph
      │
      ▼
FastAPI Webhook
      │
      ▼
Azure Queue Storage
      │
      ▼
Email Worker
      ├── Microsoft Graph
      ├── Azure SQL
      ├── SharePoint
      └── KACE
```

## Workflow

1. Microsoft Graph sends a notification when a new email arrives.
2. The webhook extracts the message ID and adds it to Azure Queue Storage.
3. A background worker consumes queued messages.
4. The email is retrieved using Microsoft Graph.
5. Azure SQL is checked for an existing conversation.
6. New conversations are routed to an available agent and create a KACE ticket.
7. Existing conversations are associated with their existing KACE ticket.
8. Successfully processed queue messages are deleted.

## Tech Stack

* Python
* FastAPI
* Microsoft Graph API
* Azure Queue Storage
* Azure SQL
* SharePoint Lists
* KACE API

## Project Structure

```text
KACE_AI_POC/
│
├── config/
│   └── settings.py   #The Primary source that reads the secrets from .env
│
├── clients/
│   ├── graph_client.py #Contains all the functions that call the Graph API
│   ├── sql_client.py   #Connects to SQL database
│   ├── kace_client.py  #Connects to the KACE API, contains HTTP methods
│   └── queue_client.py #Connects to Azure Queue Storage for async message handling
│
├── ingestion/
│   ├── webhook_receiver.py     #Validates Webhook and receives notifications
│   ├── subscription_manager.py #Creates and renews the webhook subscription
│   └── email_reader.py         #Extracts structured email data from raw data
│
├── roster/
│   ├── roster_cache.py   #Caches the SharePoint roster on application startup
│   └── roster_service.py #Provides functions to interact with the Cache
│
├── assignment/
│   ├── round_robin.py            #Runs the round-robin pointer to get the next agent
│   ├── availability_service.py   #Determines the availability of the agent
│   └── routing_service.py        #Combines round-robin and availability
│
├── worker/
│   ├── email_worker.py      #Processes the incoming emails and convert them to tickets
│   ├── sharepoint_worker.py #Gets agents from the SharePoint roster
|   ├── ooo_worker  #Gets Out of Office status for the agents
│   └── sql_worker.py        #Provides functions to read and write in the DB
│
├── models/
│   ├── agent.py       #Defines structured agent payload
│   └── email.py       #Defines structured email payload
│
├── ticketing/
│   └── ticket_service.py  #Provides function to interact with KACE
│
├── sql/
│   └── schema.sql  #Provides the schema to initialize and create tables
│
├── .env
├── cleaner.py  #Cleans emails to extract only relevant information form the body
├── main.py  
└── requirements.txt
```

## Configuration

The application requires configuration for:

* Microsoft Entra ID
* Shared mailbox
* Azure Queue Storage
* Azure SQL
* SharePoint site and roster list
* KACE

Secrets and credentials must not be committed to the repository.

## Running

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app
```

The application starts the FastAPI webhook and the background email worker.

## Production Readiness

This repository is currently a proof of concept. Before production deployment, the following changes are recommended.

### 1. Separate the Worker

Move email processing into a separate worker process or Azure Container App.

```text
Container App 1
└── FastAPI Webhook
        │
        ▼
Azure Queue Storage
        │
        ▼
Container App 2
└── Email Worker
```

The existing queue boundary allows the worker to be separated without changing the core processing logic.

### 2. Add Idempotency

Prevent duplicate ticket creation when queue messages are delivered more than once.

Recommended database constraints:

* `conversation_id` should be unique in the conversations table.
* Processed Microsoft Graph message IDs should be stored with a unique constraint.

### 3. Add Retry and Poison Message Handling

Use the Azure Queue dequeue count to identify repeatedly failing messages.

After a configured number of failed attempts, move the message to a separate poison queue for investigation instead of retrying indefinitely.

### 4. Make Routing Concurrency Safe

The current round-robin routing state should be updated atomically in Azure SQL before running multiple worker instances.

This prevents multiple workers from selecting the same routing position simultaneously.

### 5. Improve Authentication and Secret Management

Production deployments should:

* Store credentials in Azure Key Vault.
* Prefer Managed Identity where supported.
* Remove sensitive values from local configuration.
* Enable TLS certificate verification for KACE connections.
* Change Database authentication to EntraID.

### 6. Add Monitoring and Logging

Replace development logging with structured application logging and integrate with Azure Application Insights or equivalent monitoring.

Monitor:

* webhook failures
* queue depth
* processing failures
* KACE API failures
* Graph API failures
* routing failures
* poison queue messages

### 7. Add Automated Tests

Add tests for the main business rules, including:

* round-robin routing
* agent availability
* roster updates
* new conversation handling
* existing conversation handling
* queue processing

External APIs should be mocked during unit testing.

### 8. Refresh Roster Data

Refresh the SharePoint roster periodically instead of only during application startup.

Production implementations may also use change notifications if near-real-time roster updates are required.

### 9. Add Webhook Validation

Validate Microsoft Graph webhook notifications using the configured `clientState` and handle malformed notifications safely.

### 10. Harden Deployment

Before production:

* deploy through a CI/CD pipeline
* use environment-specific configuration
* restrict Azure resource permissions using least privilege
* configure health checks
* define backup and recovery procedures for Azure SQL
* document operational support and failure recovery

## Status

The current implementation validates the core email-to-ticket workflow and establishes a modular architecture that can be extended into a production deployment without redesigning the core business logic.
