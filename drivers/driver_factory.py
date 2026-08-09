from appium import webdriver
from appium.options.android import UiAutomator2Options

from config.config import (
    APPIUM_SERVER,
    PLATFORM_NAME,
    DEVICE_NAME,
    APP_PACKAGE,
    APP_ACTIVITY
)


def create_driver():

    options = UiAutomator2Options()

    options.platform_name = PLATFORM_NAME
    options.device_name = DEVICE_NAME
    options.automation_name = "UiAutomator2"

    if APP_PACKAGE:
        options.app_package = APP_PACKAGE

    if APP_ACTIVITY:
        options.app_activity = APP_ACTIVITY

    driver = webdriver.Remote(
        command_executor=APPIUM_SERVER,
        options=options
    )

    return driver