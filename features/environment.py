from database.connection import DatabaseConnection
from database.repositories.user_repository import UserRepository
from database.repositories.account_repository import AccountRepository

from api.api_client import ApiClient
from api.pokemon_api import PokemonApi
from api.test_api import TestApi

from config.api_config import (
    POKEMON_API_URL,
    TEST_API_URL
)

import allure


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

        print(
            "\n🗄️ CONECTANDO A BASE DE DATOS..."
        )

        try:

            context.db = (
                DatabaseConnection()
            )

            context.db.connect()

            context.user_repository = (
                UserRepository(
                    context.db
                )
            )

            context.account_repository = (
                AccountRepository(
                    context.db
                )
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

        print(
            "\n🌐 CONFIGURANDO APIs..."
        )

        try:

            # =================================================
            # LISTA CENTRAL DE APIS
            # =================================================

            context.api_clients = []

            # =================================================
            # POKEMON API
            # =================================================

            context.api_client = ApiClient(

                base_url=POKEMON_API_URL,

                name="PokeAPI"
            )

            context.pokemon_api = (
                PokemonApi(
                    context.api_client
                )
            )

            context.api_clients.append(
                context.api_client
            )

            # =================================================
            # TEST API
            # =================================================

            context.test_api_client = ApiClient(

                base_url=TEST_API_URL,

                name="JSONPlaceholder"
            )

            context.test_api = (
                TestApi(
                    context.test_api_client
                )
            )

            context.api_clients.append(
                context.test_api_client
            )

            # =================================================
            # LOG
            # =================================================

            print(
                "\n🌐 APIs CONFIGURADAS:"
            )

            for api in context.api_clients:

                print(
                    f"   • {api.name}"
                )

            print(
                "\n✅ APIs CONFIGURADAS"
            )

        except Exception as e:

            print(
                "\n❌ ERROR AL CONFIGURAR APIs:"
            )

            print(e)

            raise


# =============================================================
# BEFORE STEP
# =============================================================

def before_step(context, step):

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
    # IDENTIFICAR ARCHIVO DEL STEP
    # =========================================================

    step_file = ""

    try:

        step_file = (
            step.location.filename.lower()
        )

    except Exception:

        pass

    print(
        "STEP FILE:",
        step_file
    )

    # =========================================================
    # DATABASE EVIDENCE
    # =========================================================

    if hasattr(
        context,
        "db_evidence"
    ):

        evidence = context.db_evidence

        allure.attach(
            str(
                evidence.get(
                    "query"
                ) or ""
            ),
            name="SQL Query",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        allure.attach(
            str(
                evidence.get(
                    "parameters"
                ) or {}
            ),
            name="SQL Parameters",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        allure.attach(
            str(
                evidence.get(
                    "result"
                ) or []
            ),
            name="SQL Result",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        print(
            "🗄️ SQL EVIDENCE "
            "ADJUNTADA A ALLURE"
        )

        del context.db_evidence

    # =========================================================
    # API EVIDENCE
    # =========================================================

    api_client = None

    if hasattr(
        context,
        "api_clients"
    ):

        for client in context.api_clients:

            if client.has_evidence:

                api_client = client

                break

    # =========================================================
    # ADJUNTAR API EVIDENCE
    # =========================================================

    if api_client:

        evidence = (
            api_client.get_last_evidence()
        )

        print(
            "\n🌐 API CALL DETECTADA"
        )

        print(
            "API:",
            evidence.get("api")
        )

        print(
            "METHOD:",
            evidence.get("method")
        )

        print(
            "ENDPOINT:",
            evidence.get("endpoint")
        )

        # =====================================================
        # API
        # =====================================================

        allure.attach(
            str(
                evidence.get(
                    "api"
                ) or ""
            ),
            name="API",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # =====================================================
        # METHOD
        # =====================================================

        allure.attach(
            str(
                evidence.get(
                    "method"
                ) or ""
            ),
            name="API Method",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # =====================================================
        # ENDPOINT
        # =====================================================

        allure.attach(
            str(
                evidence.get(
                    "endpoint"
                ) or ""
            ),
            name="API Endpoint",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # =====================================================
        # PARAMETERS
        # =====================================================

        parameters = (
            evidence.get(
                "parameters"
            )
        )

        if parameters is None:

            parameters = {}

        allure.attach(
            str(parameters),
            name="API Parameters",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # =====================================================
        # STATUS CODE
        # =====================================================

        allure.attach(
            str(
                evidence.get(
                    "status_code"
                ) or ""
            ),
            name="API Status Code",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # =====================================================
        # RESPONSE
        # =====================================================

        response = (
            evidence.get(
                "response"
            )
        )

        if response is None:

            response = ""

        allure.attach(
            str(response),
            name="API Response",
            attachment_type=(
                allure.attachment_type.JSON
                if isinstance(
                    response,
                    (dict, list)
                )
                else allure.attachment_type.TEXT
            )
        )

        print(
            "🌐 API EVIDENCE "
            "ADJUNTADA A ALLURE"
        )

        # =====================================================
        # LIMPIAR EVIDENCIA
        # =====================================================

        api_client.clear_last_evidence()

    # =========================================================
    # ASSERTION EVIDENCE
    # =========================================================

    if hasattr(
        context,
        "assert_evidence"
    ):

        evidence = context.assert_evidence

        allure.attach(
            str(
                evidence.get(
                    "description"
                ) or "Assertion"
            ),
            name="Assertion",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        allure.attach(
            str(
                evidence.get(
                    "expected"
                ) or ""
            ),
            name="Expected",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        allure.attach(
            str(
                evidence.get(
                    "actual"
                ) or ""
            ),
            name="Actual",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        print(
            "🔎 ASSERTION EVIDENCE "
            "ADJUNTADA A ALLURE"
        )

        del context.assert_evidence

    # =========================================================
    # APPIUM SCREENSHOT
    # =========================================================

    is_api_step = (
        "api_steps.py" in step_file
    )

    is_database_step = (
        "database_steps.py" in step_file
    )

    if (
        hasattr(
            context,
            "driver"
        )
        and context.driver
        and not is_api_step
        and not is_database_step
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
                "📸 SCREENSHOT ADJUNTADO "
                f"A ALLURE: {step.name}"
            )

        except Exception as e:

            print(
                "\n❌ ERROR AL CAPTURAR "
                "SCREENSHOT DEL STEP:"
            )

            print(e)


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

    if (
        hasattr(
            context,
            "driver"
        )
        and context.driver
    ):

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