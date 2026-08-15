import os

import oracledb
from dotenv import load_dotenv


load_dotenv()


class DatabaseConnection:

    def __init__(self):

        self.connection = None

        # =====================================================
        # EVIDENCIA DE LA ÚLTIMA CONSULTA
        # =====================================================

        self.last_query = None
        self.last_parameters = None
        self.last_result = None

    # =========================================================
    # CONECTAR A ORACLE
    # =========================================================

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

            print(
                "\n🗄️ Conexión a Oracle establecida"
            )

            return self.connection

        except oracledb.Error as e:

            print(
                "\n❌ Error conectando a Oracle:"
            )

            print(e)

            raise

    # =========================================================
    # EJECUTAR QUERY
    # =========================================================

    def execute_query(self, query, params=None):

        if not self.connection:

            raise Exception(
                "❌ No existe una conexión activa "
                "a la base de datos"
            )

        cursor = self.connection.cursor()

        try:

            # =================================================
            # PARÁMETROS
            # =================================================

            parameters = params or {}

            # =================================================
            # EJECUTAR QUERY
            # =================================================

            cursor.execute(
                query,
                parameters
            )

            # =================================================
            # OBTENER RESULTADOS
            # =================================================

            results = cursor.fetchall()

            # =================================================
            # GUARDAR EVIDENCIA
            # =================================================

            self.last_query = query
            self.last_parameters = parameters
            self.last_result = results

            print(
                "\n🗄️ QUERY EJECUTADA:"
            )

            print(query)

            print(
                "\n🔧 PARAMETERS:"
            )

            print(parameters)

            print(
                "\n📋 RESULT:"
            )

            print(results)

            return results

        except oracledb.Error as e:

            print(
                "\n❌ ERROR EJECUTANDO QUERY:"
            )

            print(e)

            raise

        finally:

            cursor.close()

    # =========================================================
    # EJECUTAR QUERY - UN SOLO REGISTRO
    # =========================================================

    def execute_query_one(
        self,
        query,
        params=None
    ):

        results = self.execute_query(
            query,
            params
        )

        if results:

            return results[0]

        return None

    # =========================================================
    # CERRAR CONEXIÓN
    # =========================================================

    def close(self):

        if self.connection:

            try:

                self.connection.close()

                print(
                    "\n🗄️ Conexión a Oracle cerrada"
                )

            except oracledb.Error as e:

                print(
                    "\n❌ Error cerrando conexión:"
                )

                print(e)

            finally:

                self.connection = None