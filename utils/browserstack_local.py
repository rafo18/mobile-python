from browserstack.local import Local

from config.config import (
    BS_ACCESS_KEY,
    BS_LOCAL,
    BS_LOCAL_IDENTIFIER
)


class BrowserStackLocalManager:

    def __init__(self):

        self.local = None

    # =========================================================
    # START
    # =========================================================

    def start(self):

        # -----------------------------------------------------
        # VALIDAR SI ESTÁ HABILITADO
        # -----------------------------------------------------

        if not BS_LOCAL:

            print(
                "\nℹ️ BROWSERSTACK LOCAL DESHABILITADO"
            )

            return

        # -----------------------------------------------------
        # VALIDAR ACCESS KEY
        # -----------------------------------------------------

        if not BS_ACCESS_KEY:

            raise ValueError(
                "BS_ACCESS_KEY no está configurado "
                "en el archivo .env"
            )

        print("\n=================================")
        print("🔐 INICIANDO BROWSERSTACK LOCAL")
        print("=================================")

        print(
            f"Identifier: "
            f"{BS_LOCAL_IDENTIFIER}"
        )

        # -----------------------------------------------------
        # CREAR LOCAL
        # -----------------------------------------------------

        self.local = Local()

        # -----------------------------------------------------
        # ARGUMENTOS
        # -----------------------------------------------------

        local_arguments = {

            "key":
                BS_ACCESS_KEY,

            "forcelocal":
                "true",

            "localIdentifier":
                BS_LOCAL_IDENTIFIER
        }

        # -----------------------------------------------------
        # INICIAR TUNNEL
        # -----------------------------------------------------

        self.local.start(
            **local_arguments
        )

        # -----------------------------------------------------
        # VALIDAR ESTADO
        # -----------------------------------------------------

        if not self.local.isRunning():

            raise RuntimeError(
                "BrowserStack Local no pudo "
                "iniciarse correctamente."
            )

        print(
            "\n✅ BROWSERSTACK LOCAL CONECTADO"
        )

        print(
            f"Identifier: "
            f"{BS_LOCAL_IDENTIFIER}"
        )

    # =========================================================
    # STOP
    # =========================================================

    def stop(self):

        if not self.local:

            return

        try:

            print(
                "\n================================="
            )

            print(
                "🔐 CERRANDO BROWSERSTACK LOCAL"
            )

            print(
                "================================="
            )

            self.local.stop()

            print(
                "✅ BROWSERSTACK LOCAL CERRADO"
            )

        except Exception as e:

            print(
                "\n❌ ERROR CERRANDO "
                "BROWSERSTACK LOCAL:"
            )

            print(e)

        finally:

            self.local = None