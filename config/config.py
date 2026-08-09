import os
from dotenv import load_dotenv

load_dotenv()

APPIUM_SERVER = os.getenv(
    "APPIUM_SERVER",
    "http://127.0.0.1:4723"
)

PLATFORM_NAME = os.getenv(
    "PLATFORM_NAME",
    "Android"
)

DEVICE_NAME = os.getenv(
    "DEVICE_NAME",
    "Android"
)

APP_PACKAGE = os.getenv("APP_PACKAGE")
APP_ACTIVITY = os.getenv("APP_ACTIVITY")