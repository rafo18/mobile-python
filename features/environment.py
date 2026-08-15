import os
from datetime import datetime

import allure

from database.connection import DatabaseConnection
from database.repositories.user_repository import UserRepository
from database.repositories.account_repository import AccountRepository

from api.api_client import ApiClient
from api.pokemon_api import PokemonApi


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

            # Crear conexión
            context.db = DatabaseConnection()
            context.db.connect()

            # Crear repositories
            context.user_repository = UserRepository(
                context.db
            )

            context.account_repository = AccountRepository(
                context.db
            )

            print("✅ CONEXIÓN A BASE DE DATOS EXITOSA")

        except Exception as e:

            print("\n❌ ERROR AL CONECTAR A BASE DE DATOS:")
            print(e)

            raise

    # =========================================================
    # API
    # =========================================================

    if "api" in scenario.effective_tags:

        print("\n🌐 CONFIGURANDO API...")

        try:

            # Crear cliente API
            context.api_client = ApiClient(
                "https://pokeapi.co/api/v2"
            )

            # Crear API de Pokemon
            context.pokemon_api = PokemonApi(
                context.api_client
            )

            print("✅ API CONFIGURADA")

        except Exception as e:

            print("\n❌ ERROR AL CONFIGURAR API:")
            print(e)

            raise


def after_scenario(context, scenario):

    print("\n==============================")
    print("AFTER SCENARIO EJECUTADO")
    print("SCENARIO:", scenario.name)
    print("STATUS:", scenario.status)
    print("==============================")

    # =========================================================
    # SCREENSHOT + ALLURE
    # =========================================================

    if hasattr(context, "driver") and context.driver:

        # Capturar cualquier escenario que NO haya terminado
        # correctamente
        if scenario.status != "passed":

            os.makedirs("screenshots", exist_ok=True)

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            scenario_name = "".join(
                c
                if c.isalnum() or c in (" ", "_", "-")
                else "_"
                for c in scenario.name
            )

            screenshot_path = os.path.abspath(
                f"screenshots/"
                f"{scenario_name}_{timestamp}.png"
            )

            try:

                # -------------------------------------------------
                # Guardar screenshot físicamente
                # -------------------------------------------------

                context.driver.save_screenshot(
                    screenshot_path
                )

                print("\n📸 SCREENSHOT GUARDADO:")
                print(screenshot_path)

                # -------------------------------------------------
                # Adjuntar screenshot a Allure
                # -------------------------------------------------

                with open(
                    screenshot_path,
                    "rb"
                ) as image:

                    allure.attach(
                        image.read(),
                        name=(
                            f"Screenshot - "
                            f"{scenario.name}"
                        ),
                        attachment_type=(
                            allure.attachment_type.PNG
                        )
                    )

                print(
                    "📎 SCREENSHOT "
                    "ADJUNTADO A ALLURE"
                )

            except Exception as e:

                print(
                    "\n❌ ERROR AL GUARDAR "
                    "SCREENSHOT:"
                )

                print(e)

        # =====================================================
        # CERRAR APPIUM
        # =====================================================

        try:

            context.driver.quit()

            print("\n📱 DRIVER CERRADO")

        except Exception as e:

            print(
                "\n❌ ERROR AL CERRAR DRIVER:"
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