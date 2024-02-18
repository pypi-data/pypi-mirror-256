from pyodbc import connect


class Database:
    def __init__(self) -> None:
        self._conn = None
        pass

    def connect(self, server: str, database: str, username: str, password: str):
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};" \
            "SERVER=" + server + ";" \
            "DATABASE=" + database + ";" \
            "UID=" + username + ";" \
            "PWD=" + password + ";" \
            "Encrypt=yes;" \
            "TrustServerCertificate=no;" \
            "Connection Timeout=30;"

        self._conn = connect(conn_str)
        return True

    def disconnect(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None
        return True

    def query(self, query: str):
        cursor = self._conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

if __name__ == "__main__": # pragma: no cover
    # Example
    from keyvault import KeyVault

    vault_url = "https://diot-keyvault-dev.vault.azure.net"
    username = KeyVault(vault_url).get_secret("Database--UserId")
    password = KeyVault(vault_url).get_secret("Database--Password")

    db = Database()
    server = 'tcp:diot-sqlserver-dev.database.windows.net,1433'
    database = 'diot-db-dev'
    db.connect(server, database, username, password)

    print(db.query('SELECT * FROM [User]'))