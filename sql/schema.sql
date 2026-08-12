CREATE TABLE dbo.Conversations (
    id INT Identity(1,1) Primary KEY,
    conversation_id NVARCHAR(255) NOT NULL UNIQUE,
    agent_id INT NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

CREATE TABLE dbo.RoutingState (
    id INT Identity(1,1) PRIMARY KEY,
    department NVARCHAR(100) NOT NULL UNIQUE,
    current_order INT,
    updasted_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);