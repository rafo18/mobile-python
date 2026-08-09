import os
from datetime import datetime


def after_scenario(context, scenario):

    print("\n==============================")
    print("AFTER SCENARIO EJECUTADO")
    print("SCENARIO:", scenario.name)
    print("STATUS:", scenario.status)
    print("==============================")

    if hasattr(context, "driver") and context.driver:

        # Capturar cualquier escenario que NO haya terminado correctamente
        if scenario.status != "passed":

            os.makedirs("screenshots", exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            scenario_name = "".join(
                c if c.isalnum() or c in (" ", "_", "-") else "_"
                for c in scenario.name
            )

            screenshot_path = os.path.abspath(
                f"screenshots/{scenario_name}_{timestamp}.png"
            )

            try:
                context.driver.save_screenshot(screenshot_path)

                print("\n📸 SCREENSHOT GUARDADO:")
                print(screenshot_path)

            except Exception as e:
                print("\n❌ ERROR AL GUARDAR SCREENSHOT:")
                print(e)

        context.driver.quit()