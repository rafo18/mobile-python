import os
from dotenv import load_dotenv


load_dotenv()


# =========================================================
# EXECUTION
# =========================================================

EXECUTION_PLATFORM = os.getenv(
    "EXECUTION_PLATFORM",
    "local"
).lower()

PLATFORM_NAME = os.getenv(
    "PLATFORM_NAME",
    "Android"
)


# =========================================================
# LOCAL APPIUM
# =========================================================

APPIUM_SERVER = os.getenv(
    "APPIUM_SERVER",
    "http://127.0.0.1:4723"
)

DEVICE_NAME = os.getenv(
    "DEVICE_NAME",
    "Android"
)

APP_PACKAGE = os.getenv(
    "APP_PACKAGE"
)

APP_ACTIVITY = os.getenv(
    "APP_ACTIVITY"
)


# =========================================================
# LAMBDATEST
# =========================================================

LT_USERNAME = os.getenv(
    "LT_USERNAME"
)

LT_ACCESS_KEY = os.getenv(
    "LT_ACCESS_KEY"
)

LT_APP = os.getenv(
    "LT_APP"
)

LT_DEVICE_INDEX = int(
    os.getenv(
        "LT_DEVICE_INDEX",
        "0"
    )
)