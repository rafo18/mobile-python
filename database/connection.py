import os

import oracledb
from dotenv import load_dotenv


load_dotenv()


class DatabaseConnection:

    def __init__(self):

        self.connection = None

        # =====================================================
        # EVIDENCIA DE LA ÚLTIMA OPERACIÓN
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
    # SELECT
    # =========================================================

    def execute_query(
        self,
        query,
        params=None
    ):

        if not self.connection:

            raise Exception(
                "❌ No existe una conexión activa "
                "a la base de datos"
            )

        cursor = self.connection.cursor()

        try:

            parameters = params or {}

            # -------------------------------------------------
            # EJECUTAR QUERY
            # -------------------------------------------------

            cursor.execute(
                query,
                parameters
            )

            # -------------------------------------------------
            # OBTENER FILAS
            # -------------------------------------------------

            rows = cursor.fetchall()

            # -------------------------------------------------
            # OBTENER NOMBRES DE COLUMNAS
            # -------------------------------------------------

            columns = [
                column[0]
                for column in cursor.description
            ]

            # -------------------------------------------------
            # CONVERTIR RESULTADOS A DICCIONARIOS
            # -------------------------------------------------

            results = [
                dict(zip(columns, row))
                for row in rows
            ]

            # -------------------------------------------------
            # GUARDAR EVIDENCIA
            # -------------------------------------------------

            self.last_query = query
            self.last_parameters = parameters
            self.last_result = results

            # -------------------------------------------------
            # LOG
            # -------------------------------------------------

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
    # SELECT - UN SOLO REGISTRO
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
    # INSERT / UPDATE / DELETE
    # =========================================================

    def execute_update(
        self,
        query,
        params=None
    ):

        if not self.connection:

            raise Exception(
                "❌ No existe una conexión activa "
                "a la base de datos"
            )

        cursor = self.connection.cursor()

        try:

            parameters = params or {}

            # -------------------------------------------------
            # EJECUTAR OPERACIÓN
            # -------------------------------------------------

            cursor.execute(
                query,
                parameters
            )

            # -------------------------------------------------
            # FILAS AFECTADAS
            # -------------------------------------------------

            rows_affected = cursor.rowcount

            # -------------------------------------------------
            # CONFIRMAR CAMBIOS
            # -------------------------------------------------

            self.connection.commit()

            # -------------------------------------------------
            # GUARDAR EVIDENCIA
            # -------------------------------------------------

            self.last_query = query
            self.last_parameters = parameters

            self.last_result = (
                f"{rows_affected} fila(s) afectada(s)"
            )

            # -------------------------------------------------
            # LOG
            # -------------------------------------------------

            print(
                "\n🗄️ OPERACIÓN EJECUTADA:"
            )

            print(query)

            print(
                "\n🔧 PARAMETERS:"
            )

            print(parameters)

            print(
                "\n📋 RESULT:"
            )

            print(
                f"{rows_affected} fila(s) afectada(s)"
            )

            return rows_affected

        except oracledb.Error as e:

            # -------------------------------------------------
            # DESHACER CAMBIOS
            # -------------------------------------------------

            self.connection.rollback()

            print(
                "\n❌ ERROR EJECUTANDO "
                "OPERACIÓN:"
            )

            print(e)

            raise

        finally:

            cursor.close()

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