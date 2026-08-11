from mssql_python import connect
from config import settings

class SQLClient:
    
    def __init__(self):
        self.connection = connect(settings.azure_sql_connection_string)

    def test_connection(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        return result[0]