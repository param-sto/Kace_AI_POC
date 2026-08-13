
class SQLWorker:
    """
    Handles database operations related to email conversations.
    """
    def __init__(self, sql_client):
        """
        Initializes the worker with an SQL client.
        """
        self.sql_client = sql_client

    def get_conversation_agent(self, conversation_id: str):
        """
        Return the agent currently assigned to a conversation.
        Returns None if the conversation does not exist.
        """
        query = """
        SELECT agent_id
        FROM dbo.Conversations
        WHERE conversation_id = ?
        """
        result = self.sql_client.fetch_one(query,(conversation_id,))
        if result is None:
            return None
        return result[0]

    def create_conversation(self, conversation_id: str, agent_id: int):
        """
        Creates a new conversation and asignes it to an agent.
        """
        query = """
        INSERT INTO dbo.Conversations (
            conversation_id,
            agent_id
        )
        VALUES (?, ?)
        """

        self.sql_client.execute(query, (str(conversation_id), int(agent_id)))

    def get_routing_state(self, department: str | None):
        """
        Gets the last updated routing state.
        """
        query = """
        SELECT last_index
        FROM dbo.RoutingState
        Where department = ?
        """

        result = self.sql_client.fetch_one(query, (department,))
        if result is None:
            return None
        return result[0]

    def update_routing_state(self, department:str | None, last_index: int):
        """
        Updates the last routing state after assignment.
        """

        query = """
        UPDATE dbo.RoutingState
        SET last_index = ?,
        updated_at = SYSUTCDATETIME()
        WHERE department = ?
        """

        self.sql_client.execute(query, (int(last_index), str(department)))
