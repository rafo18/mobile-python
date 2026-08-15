from database.connection import DatabaseConnection
from database.repositories.user_repository import UserRepository
from database.repositories.account_repository import AccountRepository

from api.api_client import ApiClient
from api.pokemon_api import PokemonApi

import allure


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

            context.user_repository = UserRepository(
                context.db
            )

            context.account_repository = AccountRepository(
                context.db
            )

            print("✅ CONEXIÓN A BASE DE DATOS EXITOSA")

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

            context.api_client = ApiClient(
                "https://pokeapi.co/api/v2"
            )

            context.pokemon_api = PokemonApi(
                context.api_client
            )

            print("✅ API CONFIGURADA")

        except Exception as e:

            print(
                "\n❌ ERROR AL CONFIGURAR API:"
            )

            print(e)

            raise


def before_step(context, step):

    # No necesitamos configurar nada antes del step.
    pass


def after_step(context, step):

    print("\n--------------------------------")
    print("AFTER STEP")
    print("STEP:", step.name)
    print("STATUS:", step.status)
    print("--------------------------------")

    # =========================================================
    # DETECTAR EVIDENCIA DATABASE
    # =========================================================

    has_db_evidence = (
        hasattr(context, "db")
        and context.db
        and context.db.last_query is not None
    )

    # =========================================================
    # DETECTAR EVIDENCIA API
    # =========================================================

    has_api_evidence = hasattr(
        context,
        "api_evidence"
    )

    # =========================================================
    # DATABASE EVIDENCE
    # =========================================================

    if has_db_evidence:

        print("\n🗄️ DATABASE EVIDENCE")

        # -----------------------------------------------------
        # SQL QUERY
        # -----------------------------------------------------

        allure.attach(
            context.db.last_query,
            name="SQL Query",
            attachment_type=allure.attachment_type.TEXT
        )

        # -----------------------------------------------------
        # PARAMETERS
        # -----------------------------------------------------

        allure.attach(
            str(
                context.db.last_parameters
            ),
            name="SQL Parameters",
            attachment_type=allure.attachment_type.TEXT
        )

        # -----------------------------------------------------
        # RESULT
        # -----------------------------------------------------

        allure.attach(
            str(
                context.db.last_result
            ),
            name="SQL Result",
            attachment_type=allure.attachment_type.TEXT
        )

        print(
            "✅ SQL EVIDENCE "
            "ADJUNTADA A ALLURE"
        )

    # =========================================================
    # API EVIDENCE
    # =========================================================

    if has_api_evidence:

        print("\n🌐 API EVIDENCE")

        evidence = context.api_evidence

        # -----------------------------------------------------
        # METHOD
        # -----------------------------------------------------

        allure.attach(
            evidence.get(
                "method",
                ""
            ),
            name="API Method",
            attachment_type=allure.attachment_type.TEXT
        )

        # -----------------------------------------------------
        # ENDPOINT
        # -----------------------------------------------------

        allure.attach(
            evidence.get(
                "endpoint",
                ""
            ),
            name="API Endpoint",
            attachment_type=allure.attachment_type.TEXT
        )

        # -----------------------------------------------------
        # PARAMETERS
        # -----------------------------------------------------

        allure.attach(
            str(
                evidence.get(
                    "parameters",
                    {}
                )
            ),
            name="API Parameters",
            attachment_type=allure.attachment_type.TEXT
        )

        # -----------------------------------------------------
        # STATUS CODE
        # -----------------------------------------------------

        allure.attach(
            str(
                evidence.get(
                    "status_code",
                    ""
                )
            ),
            name="API Status Code",
            attachment_type=allure.attachment_type.TEXT
        )

        # -----------------------------------------------------
        # RESPONSE
        # -----------------------------------------------------

        response = evidence.get(
            "response",
            ""
        )

        if isinstance(
            response,
            (dict, list)
        ):

            allure.attach(
                str(response),
                name="API Response",
                attachment_type=allure.attachment_type.JSON
            )

        else:

            allure.attach(
                str(response),
                name="API Response",
                attachment_type=allure.attachment_type.TEXT
            )

        print(
            "✅ API EVIDENCE "
            "ADJUNTADA A ALLURE"
        )

        # Limpiar evidencia API
        del context.api_evidence

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
            attachment_type=allure.attachment_type.TEXT
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
            attachment_type=allure.attachment_type.TEXT
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
            attachment_type=allure.attachment_type.TEXT
        )

        print(
            "✅ ASSERTION EVIDENCE "
            "ADJUNTADA A ALLURE"
        )

        # Limpiar evidencia
        del context.assert_evidence

    # =========================================================
    # APPIUM SCREENSHOT
    # =========================================================
    #
    # Screenshot SOLO cuando:
    #
    # 1. Existe driver
    # 2. NO hubo consulta DB
    # 3. NO hubo evidencia API
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


def after_scenario(context, scenario):

    print("\n==============================")
    print("AFTER SCENARIO EJECUTADO")
    print("SCENARIO:", scenario.name)
    print("STATUS:", scenario.status)
    print("==============================")

    # =========================================================
    # CERRAR APPIUM
    # =========================================================

    if hasattr(context, "driver") and context.driver:

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

    if hasattr(context, "db"):

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

    print("\n==============================")
    print("FIN DEL SCENARIO")
    print("==============================\n")