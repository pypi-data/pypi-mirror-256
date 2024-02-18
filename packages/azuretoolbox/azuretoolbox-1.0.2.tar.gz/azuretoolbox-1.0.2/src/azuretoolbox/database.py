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

    def __parse__(self, response: list, header: list) -> list[dict]:
        result = []
        for row in response:
            temp = {}
            for i in range(len(header)):
                temp[header[i][0]] = row[i]
            result.append(temp)
        return result

    def query(self, query: str):
        cursor = self._conn.cursor()
        cursor.execute(query)
        response = cursor.fetchall()
        return self.__parse__(response, cursor.description)
