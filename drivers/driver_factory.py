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

    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY

    options.app_wait_activity = "*"

    options.new_command_timeout = 120

    options.no_reset = False

    driver = webdriver.Remote(
        command_executor=APPIUM_SERVER,
        options=options
    )

    return driver