import allure

from database.connection import DatabaseConnection
from database.repositories.user_repository import UserRepository
from database.repositories.account_repository import AccountRepository

from api.api_client import ApiClient
from api.pokemon_api import PokemonApi


# =============================================================
# BEFORE SCENARIO
# =============================================================

def before_scenario(context, scenario):

    print("\n==============================")
    print("BEFORE SCENARIO EJECUTADO")
    print("SCENARIO:", scenario.name)
    print("==============================")

    # =========================================================
    # DATABASE
    # =========================================================

    if "database" in scenario.effective_tags:

        print("\n🗄️ CONECTANDO A BASE DE DATOS...")

        try:

            context.db = DatabaseConnection()

            context.db.connect()

            # -------------------------------------------------
            # REPOSITORIES
            # -------------------------------------------------

            context.user_repository = UserRepository(
                context.db
            )

            context.account_repository = AccountRepository(
                context.db
            )

            print(
                "✅ CONEXIÓN A BASE DE DATOS EXITOSA"
            )

        except Exception as e:

            print(
                "\n❌ ERROR AL CONECTAR "
                "A BASE DE DATOS:"
            )

            print(e)

            raise

    # =========================================================
    # API
    # =========================================================

    if "api" in scenario.effective_tags:

        print("\n🌐 CONFIGURANDO API...")

        try:

            # -------------------------------------------------
            # API CLIENT
            # -------------------------------------------------

            context.api_client = ApiClient(
                "https://pokeapi.co/api/v2"
            )

            # -------------------------------------------------
            # POKEMON API
            # -------------------------------------------------

            context.pokemon_api = PokemonApi(
                context.api_client
            )

            print(
                "✅ API CONFIGURADA"
            )

        except Exception as e:

            print(
                "\n❌ ERROR AL CONFIGURAR API:"
            )

            print(e)

            raise


# =============================================================
# BEFORE STEP
# =============================================================

def before_step(context, step):

    # No necesitamos configurar nada.
    pass


# =============================================================
# AFTER STEP
# =============================================================

def after_step(context, step):

    print("\n--------------------------------")
    print("AFTER STEP")
    print("STEP:", step.name)
    print("STATUS:", step.status)
    print("--------------------------------")

    # =========================================================
    # DATABASE EVIDENCE
    # =========================================================

    has_db_evidence = (
        hasattr(context, "db")
        and context.db
        and context.db.last_query is not None
    )

    if has_db_evidence:

        print("\n🗄️ DATABASE EVIDENCE")

        # -----------------------------------------------------
        # QUERY
        # -----------------------------------------------------

        allure.attach(
            context.db.last_query,
            name="SQL Query",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # PARAMETERS
        # -----------------------------------------------------

        allure.attach(
            str(
                context.db.last_parameters
            ),
            name="SQL Parameters",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # RESULT
        # -----------------------------------------------------

        allure.attach(
            str(
                context.db.last_result
            ),
            name="SQL Result",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        print(
            "✅ SQL EVIDENCE "
            "ADJUNTADA A ALLURE"
        )

    # =========================================================
    # API EVIDENCE
    # =========================================================

    has_api_evidence = (
        hasattr(context, "api_client")
        and context.api_client
        and context.api_client.last_endpoint is not None
    )

    if has_api_evidence:

        print("\n🌐 API EVIDENCE")

        # -----------------------------------------------------
        # METHOD
        # -----------------------------------------------------

        allure.attach(
            context.api_client.last_method,
            name="API Method",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # ENDPOINT
        # -----------------------------------------------------

        allure.attach(
            context.api_client.last_endpoint,
            name="API Endpoint",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # PARAMETERS
        # -----------------------------------------------------

        allure.attach(
            str(
                context.api_client.last_parameters
            ),
            name="API Parameters",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # STATUS CODE
        # -----------------------------------------------------

        allure.attach(
            str(
                context.api_client.last_status_code
            ),
            name="API Status Code",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # RESPONSE
        # -----------------------------------------------------

        response = context.api_client.last_response

        if isinstance(
            response,
            (dict, list)
        ):

            allure.attach(
                str(response),
                name="API Response",
                attachment_type=(
                    allure.attachment_type.JSON
                )
            )

        else:

            allure.attach(
                str(response),
                name="API Response",
                attachment_type=(
                    allure.attachment_type.TEXT
                )
            )

        print(
            "✅ API EVIDENCE "
            "ADJUNTADA A ALLURE"
        )

    # =========================================================
    # ASSERTION EVIDENCE
    # =========================================================

    if hasattr(
        context,
        "assert_evidence"
    ):

        print("\n🔎 ASSERTION EVIDENCE")

        evidence = context.assert_evidence

        # -----------------------------------------------------
        # DESCRIPTION
        # -----------------------------------------------------

        allure.attach(
            str(
                evidence.get(
                    "description",
                    "Assertion"
                )
            ),
            name="Assertion",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # EXPECTED
        # -----------------------------------------------------

        allure.attach(
            str(
                evidence.get(
                    "expected",
                    ""
                )
            ),
            name="Expected",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # ACTUAL
        # -----------------------------------------------------

        allure.attach(
            str(
                evidence.get(
                    "actual",
                    ""
                )
            ),
            name="Actual",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        print(
            "✅ ASSERTION EVIDENCE "
            "ADJUNTADA A ALLURE"
        )

        # -----------------------------------------------------
        # LIMPIAR ASSERTION
        # -----------------------------------------------------

        del context.assert_evidence

    # =========================================================
    # APPIUM SCREENSHOT
    # =========================================================
    #
    # Se captura solamente cuando el step:
    #
    # - Tiene Appium disponible
    # - NO ejecutó una consulta SQL
    # - NO ejecutó una llamada API
    #
    # =========================================================

    if (
        hasattr(context, "driver")
        and context.driver
        and not has_db_evidence
        and not has_api_evidence
    ):

        try:

            screenshot = (
                context.driver
                .get_screenshot_as_png()
            )

            allure.attach(
                screenshot,
                name=(
                    f"Screenshot - "
                    f"{step.name}"
                ),
                attachment_type=(
                    allure.attachment_type.PNG
                )
            )

            print(
                "📸 SCREENSHOT "
                "ADJUNTADO A ALLURE"
            )

        except Exception as e:

            print(
                "\n❌ ERROR AL CAPTURAR "
                "SCREENSHOT:"
            )

            print(e)

    # =========================================================
    # LIMPIAR EVIDENCIA DATABASE
    # =========================================================

    if hasattr(context, "db"):

        context.db.last_query = None
        context.db.last_parameters = None
        context.db.last_result = None

    # =========================================================
    # LIMPIAR EVIDENCIA API
    # =========================================================

    if hasattr(context, "api_client"):

        context.api_client.last_method = None
        context.api_client.last_endpoint = None
        context.api_client.last_parameters = None
        context.api_client.last_status_code = None
        context.api_client.last_response = None


# =============================================================
# AFTER SCENARIO
# =============================================================

def after_scenario(context, scenario):

    print("\n==============================")
    print("AFTER SCENARIO EJECUTADO")
    print("SCENARIO:", scenario.name)
    print("STATUS:", scenario.status)
    print("==============================")

    # =========================================================
    # CERRAR APPIUM
    # =========================================================

    if hasattr(
        context,
        "driver"
    ) and context.driver:

        try:

            context.driver.quit()

            print(
                "\n📱 DRIVER CERRADO"
            )

        except Exception as e:

            print(
                "\n❌ ERROR AL CERRAR "
                "DRIVER:"
            )

            print(e)

    # =========================================================
    # CERRAR DATABASE
    # =========================================================

    if hasattr(
        context,
        "db"
    ):

        try:

            context.db.close()

            print(
                "\n🗄️ CONEXIÓN A BASE DE DATOS "
                "CERRADA"
            )

        except Exception as e:

            print(
                "\n❌ ERROR AL CERRAR "
                "BASE DE DATOS:"
            )

            print(e)

    print(
        "\n=============================="
    )

    print(
        "FIN DEL SCENARIO"
    )

    print(
        "==============================\n"
    )