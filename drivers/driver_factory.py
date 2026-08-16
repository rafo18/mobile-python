from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

from config.config import (
    EXECUTION_PLATFORM,

    # LOCAL
    APPIUM_SERVER,
    PLATFORM_NAME,
    DEVICE_NAME,
    APP_PACKAGE,
    APP_ACTIVITY,

    # LAMBDATEST
    LT_USERNAME,
    LT_ACCESS_KEY,
    LT_APP,
    LT_DEVICE_INDEX
)

from config.devices import (
    ANDROID_DEVICES,
    IOS_DEVICES
)


def create_driver():

    platform = PLATFORM_NAME.lower()

    # =========================================================
    # LOCAL
    # =========================================================

    if EXECUTION_PLATFORM == "local":

        return create_local_driver(
            platform
        )

    # =========================================================
    # LAMBDATEST
    # =========================================================

    elif EXECUTION_PLATFORM == "lambdatest":

        return create_lambdatest_driver(
            platform
        )

    else:

        raise ValueError(
            f"Plataforma de ejecución no soportada: "
            f"{EXECUTION_PLATFORM}"
        )


# =============================================================
# LOCAL
# =============================================================

def create_local_driver(platform):

    # ---------------------------------------------------------
    # ANDROID
    # ---------------------------------------------------------

    if platform == "android":

        options = UiAutomator2Options()

        options.platform_name = "Android"
        options.device_name = DEVICE_NAME
        options.automation_name = "UiAutomator2"

        options.app_package = APP_PACKAGE
        options.app_activity = APP_ACTIVITY

        options.app_wait_activity = "*"

        options.new_command_timeout = 120

        options.no_reset = False

    # ---------------------------------------------------------
    # IOS
    # ---------------------------------------------------------

    elif platform == "ios":

        options = XCUITestOptions()

        options.platform_name = "iOS"
        options.device_name = DEVICE_NAME
        options.automation_name = "XCUITest"

        options.new_command_timeout = 120

        options.no_reset = False

    else:

        raise ValueError(
            f"Plataforma móvil no soportada: "
            f"{PLATFORM_NAME}"
        )

    driver = webdriver.Remote(
        command_executor=APPIUM_SERVER,
        options=options
    )

    return driver


# =============================================================
# LAMBDATEST
# =============================================================

def create_lambdatest_driver(platform):

    # =========================================================
    # OBTENER DISPOSITIVO
    # =========================================================
    
    if platform == "android":

        devices = ANDROID_DEVICES

    elif platform == "ios":

        devices = IOS_DEVICES

    else:

        raise ValueError(
            f"Plataforma móvil no soportada: "
            f"{PLATFORM_NAME}"
        )

    # =========================================================
    # VALIDAR INDEX
    # =========================================================

    if LT_DEVICE_INDEX < 0:

        raise ValueError(
            "LT_DEVICE_INDEX no puede ser negativo"
        )

    if LT_DEVICE_INDEX >= len(devices):

        raise ValueError(
            f"LT_DEVICE_INDEX={LT_DEVICE_INDEX} "
            f"no existe. "
            f"Hay {len(devices)} dispositivos configurados."
        )

    # =========================================================
    # DISPOSITIVO SELECCIONADO
    # =========================================================

    device = devices[LT_DEVICE_INDEX]

    device_name = device["name"]

    platform_version = device[
        "platform_version"
    ]

    print("\n=================================")
    print("📱 LAMBDATEST DEVICE")
    print("=================================")
    print(f"Device: {device_name}")
    print(f"Platform: {platform}")
    print(f"Version: {platform_version}")
    print(f"Index: {LT_DEVICE_INDEX}")
    print("=================================\n")

    print(
        "\n📱 DISPOSITIVO SELECCIONADO:"
    )

    print(
        f"   Device: {device_name}"
    )

    print(
        f"   OS: {platform} {platform_version}"
    )

    # =========================================================
    # ANDROID
    # =========================================================

    if platform == "android":

        options = UiAutomator2Options()

        options.load_capabilities({

            "platformName": "Android",

            "appium:deviceName":
                device_name,

            "appium:platformVersion":
                platform_version,

            "appium:automationName":
                "UiAutomator2",

            "appium:app":
                LT_APP,

            "appium:noReset":
                False,

            "appium:newCommandTimeout":
                120,

            "isRealMobile":
                True,

            "tunnel": 
                False,

            "build":
                "Mobile Automation",

            "name":
                f"Android - {device_name}",

            "video":
                True,

            "visual":
                True,

            "network":
                True,

            "deviceLog":
                True
        })

    # =========================================================
    # IOS
    # =========================================================

    else:

        options = XCUITestOptions()

        options.load_capabilities({

            "platformName": "iOS",

            "appium:deviceName":
                device_name,

            "appium:platformVersion":
                platform_version,

            "appium:automationName":
                "XCUITest",

            "appium:app":
                LT_APP,

            "appium:noReset":
                False,

            "appium:newCommandTimeout":
                120,

            "isRealMobile":
                True,

            "build":
                "Mobile Automation",

            "name":
                f"iOS - {device_name}",

            "video":
                True,

            "visual":
                True,

            "network":
                True,

            "deviceLog":
                True
        })

    # =========================================================
    # LAMBDATEST HUB
    # =========================================================

    command_executor = (
        f"https://{LT_USERNAME}:"
        f"{LT_ACCESS_KEY}"
        "@mobile-hub.lambdatest.com/wd/hub"
    )

    # =========================================================
    # CREAR DRIVER
    # =========================================================

    driver = webdriver.Remote(
        command_executor=command_executor,
        options=options
    )

    return driver