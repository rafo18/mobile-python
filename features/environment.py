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
import json


# =============================================================
# ALLURE - ATTACH SEGURO
# =============================================================

def safe_allure_attach(
    body,
    name,
    attachment_type=allure.attachment_type.TEXT
):
    """
    Adjunta información a Allure evitando errores cuando
    el valor recibido sea None.
    """

    if body is None:
        body = ""

    # ---------------------------------------------------------
    # JSON
    # ---------------------------------------------------------

    if attachment_type == allure.attachment_type.JSON:

        if isinstance(body, (dict, list)):

            body = json.dumps(
                body,
                indent=4,
                ensure_ascii=False,
                default=str
            )

        else:

            body = str(body)

    # ---------------------------------------------------------
    # TEXT
    # ---------------------------------------------------------

    elif not isinstance(body, (bytes, bytearray)):

        body = str(body)

    allure.attach(
        body,
        name=name,
        attachment_type=attachment_type
    )


# =============================================================
# ALLURE - INFORMACIÓN DEL DISPOSITIVO
# =============================================================

def add_device_information_to_allure(context):

    platform = PLATFORM_NAME.lower()

    # =========================================================
    # EJECUCIÓN LOCAL
    # =========================================================

    if EXECUTION_PLATFORM == "local":

        allure.dynamic.parameter(
            "Device",
            "Local - " + str(
                getattr(
                    context,
                    "device_name",
                    "Local Device"
                )
            )
        )

        allure.dynamic.parameter(
            "Platform",
            PLATFORM_NAME
        )

        allure.dynamic.parameter(
            "Execution",
            EXECUTION_PLATFORM
        )

        return

    # =========================================================
    # OBTENER LISTA DE DISPOSITIVOS
    # =========================================================

    if platform == "android":

        devices = ANDROID_DEVICES

    elif platform == "ios":

        devices = IOS_DEVICES

    else:

        return

    # =========================================================
    # VALIDAR INDEX
    # =========================================================

    if LT_DEVICE_INDEX < 0:

        return

    if LT_DEVICE_INDEX >= len(devices):

        return

    # =========================================================
    # DISPOSITIVO ACTUAL
    # =========================================================

    device = devices[
        LT_DEVICE_INDEX
    ]

    device_name = device[
        "name"
    ]

    platform_version = device[
        "platform_version"
    ]

    # =========================================================
    # ALLURE PARAMETERS
    # =========================================================

    allure.dynamic.parameter(
        "Device",
        device_name
    )

    allure.dynamic.parameter(
        "Platform",
        PLATFORM_NAME
    )

    allure.dynamic.parameter(
        "Version",
        platform_version
    )

    allure.dynamic.parameter(
        "Execution",
        EXECUTION_PLATFORM
    )


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

    print("\n--------------------------------")
    print("BEFORE STEP")
    print("STEP:", step.name)
    print("--------------------------------")

    # =========================================================
    # LIMPIAR EVIDENCIA DE DATABASE
    # =========================================================
    #
    # IMPORTANTE:
    #
    # Si el step anterior hizo una consulta SQL, no queremos
    # que el siguiente step crea que también hizo una consulta.
    # =========================================================

    if hasattr(
        context,
        "db"
    ) and context.db:

        context.db.last_query = None
        context.db.last_parameters = None
        context.db.last_result = None

    # =========================================================
    # LIMPIAR EVIDENCIA API
    # =========================================================
    #
    # De la misma manera limpiamos la información de la
    # última llamada API.
    # =========================================================

    if hasattr(
        context,
        "api_client"
    ) and context.api_client:

        context.api_client.last_method = None
        context.api_client.last_endpoint = None
        context.api_client.last_parameters = None
        context.api_client.last_status_code = None
        context.api_client.last_response = None

        # Estos atributos pueden existir si posteriormente
        # los agregamos al ApiClient.

        if hasattr(
            context.api_client,
            "last_headers"
        ):

            context.api_client.last_headers = None

        if hasattr(
            context.api_client,
            "last_body"
        ):

            context.api_client.last_body = None

    # =========================================================
    # ALLURE - DEVICE INFORMATION
    # =========================================================

    if not hasattr(
        context,
        "_allure_device_info_added"
    ):

        add_device_information_to_allure(
            context
        )

        context._allure_device_info_added = True


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
    # DETECTAR DATABASE
    # =========================================================
    #
    # NO necesitamos:
    #
    # context.step_type = "database"
    #
    # Si last_query tiene información significa que este step
    # ejecutó una operación SQL.
    # =========================================================

    has_db_evidence = (
        hasattr(
            context,
            "db"
        )
        and context.db
        and context.db.last_query is not None
    )

    # =========================================================
    # DETECTAR API
    # =========================================================
    #
    # Si last_method tiene información significa que este step
    # realizó una llamada API.
    # =========================================================

    has_api_evidence = (
        hasattr(
            context,
            "api_client"
        )
        and context.api_client
        and context.api_client.last_method is not None
    )

    print(
        "🗄️ DB EVIDENCE:",
        has_db_evidence
    )

    print(
        "🌐 API EVIDENCE:",
        has_api_evidence
    )

    # =========================================================
    # DATABASE EVIDENCE
    # =========================================================

    if has_db_evidence:

        print(
            "\n🗄️ GENERANDO EVIDENCIA SQL..."
        )

        # -----------------------------------------------------
        # QUERY
        # -----------------------------------------------------

        safe_allure_attach(
            context.db.last_query,
            name="SQL Query",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # PARAMETERS
        # -----------------------------------------------------

        safe_allure_attach(
            context.db.last_parameters,
            name="SQL Parameters",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # RESULT
        # -----------------------------------------------------

        safe_allure_attach(
            context.db.last_result,
            name="SQL Result",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        print(
            "✅ SQL EVIDENCE ADJUNTADA A ALLURE"
        )

    # =========================================================
    # API EVIDENCE
    # =========================================================

    if has_api_evidence:

        print(
            "\n🌐 GENERANDO EVIDENCIA API..."
        )

        api_client = context.api_client

        # -----------------------------------------------------
        # METHOD
        # -----------------------------------------------------

        safe_allure_attach(
            api_client.last_method,
            name="API Method",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # ENDPOINT
        # -----------------------------------------------------

        safe_allure_attach(
            api_client.last_endpoint,
            name="API Endpoint",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # PARAMETERS
        # -----------------------------------------------------

        safe_allure_attach(
            api_client.last_parameters,
            name="API Parameters",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # HEADERS
        # -----------------------------------------------------

        if hasattr(
            api_client,
            "last_headers"
        ):

            safe_allure_attach(
                api_client.last_headers,
                name="API Headers",
                attachment_type=(
                    allure.attachment_type.JSON
                )
            )

        # -----------------------------------------------------
        # BODY
        # -----------------------------------------------------

        if hasattr(
            api_client,
            "last_body"
        ):

            safe_allure_attach(
                api_client.last_body,
                name="API Body",
                attachment_type=(
                    allure.attachment_type.JSON
                )
            )

        # -----------------------------------------------------
        # STATUS CODE
        # -----------------------------------------------------

        safe_allure_attach(
            api_client.last_status_code,
            name="API Status Code",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # RESPONSE
        # -----------------------------------------------------

        response = api_client.last_response

        if isinstance(
            response,
            (dict, list)
        ):

            safe_allure_attach(
                response,
                name="API Response",
                attachment_type=(
                    allure.attachment_type.JSON
                )
            )

        else:

            safe_allure_attach(
                response,
                name="API Response",
                attachment_type=(
                    allure.attachment_type.TEXT
                )
            )

        print(
            "✅ API EVIDENCE ADJUNTADA A ALLURE"
        )

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

        safe_allure_attach(
            evidence.get(
                "description",
                "Assertion"
            ),
            name="Assertion",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # EXPECTED
        # -----------------------------------------------------

        safe_allure_attach(
            evidence.get(
                "expected",
                ""
            ),
            name="Expected",
            attachment_type=(
                allure.attachment_type.TEXT
            )
        )

        # -----------------------------------------------------
        # ACTUAL
        # -----------------------------------------------------

        safe_allure_attach(
            evidence.get(
                "actual",
                ""
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
    #
    # REGLA:
    #
    # Database → SQL Evidence → NO SCREENSHOT
    #
    # API      → API Evidence → NO SCREENSHOT
    #
    # Mobile   → Screenshot
    #
    # No importa en qué archivo esté definido el step.
    # =========================================================

    is_non_mobile_step = (
        has_db_evidence
        or has_api_evidence
    )

    if (
        hasattr(
            context,
            "driver"
        )
        and context.driver
        and not is_non_mobile_step
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

    else:

        print(
            "ℹ️ SCREENSHOT OMITIDO"
        )

        if has_db_evidence:

            print(
                "   Motivo: STEP DE BASE DE DATOS"
            )

        elif has_api_evidence:

            print(
                "   Motivo: STEP DE API"
            )


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

        finally:

            context.driver = None

    # =========================================================
    # CERRAR DATABASE
    # =========================================================

    if (
        hasattr(
            context,
            "db"
        )
        and context.db
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

        finally:

            context.db = None

    # =========================================================
    # FIN
    # =========================================================

    print("\n==============================")
    print("FIN DEL SCENARIO")
    print("==============================\n")