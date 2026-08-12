from mssql_python import connect
from config import settings

class SQLClient:
    
    def __init__(self):
        """
        Establishes connection to the SQL server Database.
        """
        self.connection = connect(settings.azure_sql_connection_string)

    def fetch_one(self, query: str, params=None):
        """
        Executes teh query and returns the first matching row.
        """
        connection = self.connection
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchone()
        finally:
            cursor.close()

    def execute(self, query: str, params=None):
        """
        Execute a database modification query and commit the transaction.
        Rolls back the transaction if the query fails.
        """
        connection = self.connection
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def close(self):
        """
        Closes the databse connection.
        """
        self.connection.close()