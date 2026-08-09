import os
from datetime import datetime


def after_scenario(context, scenario):

    if hasattr(context, "driver"):

        if scenario.status == "failed":

            os.makedirs("screenshots", exist_ok=True)

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            screenshot_path = (
                f"screenshots/{scenario.name}_{timestamp}.png"
            )

            context.driver.save_screenshot(
                screenshot_path
            )

            print(
                f"\nScreenshot guardado: {screenshot_path}"
            )

        context.driver.quit()