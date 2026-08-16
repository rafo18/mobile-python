from database.connection import DatabaseConnection
from database.repositories.user_repository import UserRepository
from database.repositories.account_repository import AccountRepository

from api.api_client import ApiClient
from api.pokemon_api import PokemonApi

from config.config import (
    EXECUTION_PLATFORM,
    PLATFORM_NAME,
    LT_DEVICE_INDEX
)

from config.devices import (
    ANDROID_DEVICES,
    IOS_DEVICES
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

        print("\n🗄️ CONECTANDO A BASE DE DATOS...")

        try:

            # -------------------------------------------------
            # CREAR CONEXIÓN
            # -------------------------------------------------

            context.db = DatabaseConnection()

            context.db.connect()

            # -------------------------------------------------
            # CREAR REPOSITORIES
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
            # CREAR CLIENTE API
            # -------------------------------------------------

            context.api_client = ApiClient(
                "https://pokeapi.co/api/v2"
            )

            # -------------------------------------------------
            # CREAR API POKEMON
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

        # -----------------------------------------------------
        # QUERY
        # -----------------------------------------------------

        allure.attach(
            evidence.get(
                "query",
                ""
            ),
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
                evidence.get(
                    "parameters",
                    {}
                )
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
                evidence.get(
                    "result",
                    []
                )
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

    if hasattr(
        context,
        "api_evidence"
    ):

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
            attachment_type=(
                allure.attachment_type.TEXT
            )
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
            attachment_type=(
                allure.attachment_type.TEXT
            )
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
            attachment_type=(
                allure.attachment_type.TEXT
            )
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
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # RESPONSE
        # -----------------------------------------------------

        response = evidence.get(
            "response",
            ""
        )

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

        del context.api_evidence

    # =========================================================
    # ASSERTION EVIDENCE
    # =========================================================

    if hasattr(
        context,
        "assert_evidence"
    ):

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

    print("\n==============================")
    print("FIN DEL SCENARIO")
    print("==============================\n")