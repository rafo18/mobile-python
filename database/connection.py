import os

import oracledb
from dotenv import load_dotenv


load_dotenv()


class DatabaseConnection:

    def __init__(self):

        self.connection = None

    def connect(self):

        if self.connection:
            return self.connection

        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT", "1521")
        service_name = os.getenv("DB_SERVICE")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

        if not all([
            host,
            port,
            service_name,
            user,
            password
        ]):
            raise ValueError(
                "Faltan variables de configuración de la base de datos "
                "en el archivo .env"
            )

        dsn = oracledb.makedsn(
            host,
            int(port),
            service_name=service_name
        )

        try:

            self.connection = oracledb.connect(
                user=user,
                password=password,
                dsn=dsn
            )

            print("\n🗄️ Conexión a Oracle establecida")

            return self.connection

        except oracledb.Error as e:

            print("\n❌ Error conectando a Oracle:")
            print(e)

            raise

    def close(self):

        if self.connection:

            try:

                self.connection.close()

                print("\n🗄️ Conexión a Oracle cerrada")

            except oracledb.Error as e:

                print("\n❌ Error cerrando conexión:")
                print(e)

            finally:

                self.connection = None

    def execute_query(self, query, params=None):

        if not self.connection:
            raise RuntimeError(
                "No existe una conexión activa con la base de datos."
            )

        cursor = self.connection.cursor()

        try:

            cursor.execute(
                query,
                params or {}
            )

            columns = [
                column[0]
                for column in cursor.description
            ]

            rows = cursor.fetchall()

            return [
                dict(zip(columns, row))
                for row in rows
            ]

        finally:

            cursor.close()

    def execute_query_one(self, query, params=None):

        results = self.execute_query(
            query,
            params
        )

        if results:
            return results[0]

        return None