from appium import webdriver

from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

from config.config import (
    # =========================================================
    # EXECUTION
    # =========================================================
    EXECUTION_PLATFORM,
    LT_TUNNEL,
    PLATFORM_NAME,

    # =========================================================
    # LOCAL
    # =========================================================
    APPIUM_SERVER,
    DEVICE_NAME,
    APP_PACKAGE,
    APP_ACTIVITY,

    # =========================================================
    # LAMBDATEST
    # =========================================================
    LT_USERNAME,
    LT_ACCESS_KEY,
    LT_APP,
    LT_DEVICE_INDEX,

    # =========================================================
    # BROWSERSTACK
    # =========================================================
    BS_USERNAME,
    BS_ACCESS_KEY,
    BS_APP,
    BS_DEVICE_INDEX,

    # =========================================================
    # BROWSERSTACK LOCAL
    # =========================================================
    BS_LOCAL,
    BS_LOCAL_IDENTIFIER
)

from config.devices import (
    # =========================================================
    # LAMBDATEST
    # =========================================================
    LAMBDATEST_ANDROID_DEVICES,
    LAMBDATEST_IOS_DEVICES,

    # =========================================================
    # BROWSERSTACK
    # =========================================================
    BROWSERSTACK_ANDROID_DEVICES,
    BROWSERSTACK_IOS_DEVICES
)


# =============================================================
# CREATE DRIVER
# =============================================================

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

    # =========================================================
    # BROWSERSTACK
    # =========================================================

    elif EXECUTION_PLATFORM == "browserstack":

        return create_browserstack_driver(
            platform
        )

    # =========================================================
    # NO SOPORTADO
    # =========================================================

    else:

        raise ValueError(
            f"Plataforma de ejecución no soportada: "
            f"{EXECUTION_PLATFORM}"
        )


# =============================================================
# LOCAL APPIUM
# =============================================================

def create_local_driver(platform):

    print("\n=================================")
    print("💻 LOCAL APPIUM")
    print("=================================")
    print(f"Platform: {platform}")
    print(f"Device: {DEVICE_NAME}")
    print("=================================\n")

    # =========================================================
    # ANDROID
    # =========================================================

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

    # =========================================================
    # IOS
    # =========================================================

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

    # =========================================================
    # CREAR DRIVER
    # =========================================================

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
    # OBTENER DISPOSITIVOS
    # =========================================================

    if platform == "android":

        devices = LAMBDATEST_ANDROID_DEVICES

    elif platform == "ios":

        devices = LAMBDATEST_IOS_DEVICES

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
    # DISPOSITIVO
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
    # LOG
    # =========================================================

    print("\n=================================")
    print("📱 LAMBDATEST")
    print("=================================")
    print(f"Device: {device_name}")
    print(f"Platform: {platform}")
    print(f"Version: {platform_version}")
    print(f"Index: {LT_DEVICE_INDEX}")
    print("=================================\n")

    # =========================================================
    # ANDROID
    # =========================================================

    if platform == "android":

        options = UiAutomator2Options()

        options.load_capabilities({

            "platformName":
                "Android",

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
                LT_TUNNEL,

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

            "platformName":
                "iOS",

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


# =============================================================
# BROWSERSTACK
# =============================================================

def create_browserstack_driver(platform):

    # =========================================================
    # VALIDAR CREDENCIALES
    # =========================================================

    if not BS_USERNAME:

        raise ValueError(
            "BS_USERNAME no está configurado "
            "en el archivo .env"
        )

    if not BS_ACCESS_KEY:

        raise ValueError(
            "BS_ACCESS_KEY no está configurado "
            "en el archivo .env"
        )

    if not BS_APP:

        raise ValueError(
            "BS_APP no está configurado "
            "en el archivo .env"
        )

    # =========================================================
    # LOG BROWSERSTACK LOCAL
    # =========================================================

    print("\n=================================")
    print("🌐 BROWSERSTACK LOCAL CONFIG")
    print("=================================")

    print(
        f"BS_LOCAL: {BS_LOCAL}"
    )

    print(
        f"BS_LOCAL_IDENTIFIER: "
        f"{BS_LOCAL_IDENTIFIER}"
    )

    print("=================================\n")

    # =========================================================
    # OBTENER DISPOSITIVOS
    # =========================================================

    if platform == "android":

        devices = BROWSERSTACK_ANDROID_DEVICES

    elif platform == "ios":

        devices = BROWSERSTACK_IOS_DEVICES

    else:

        raise ValueError(
            f"Plataforma móvil no soportada: "
            f"{PLATFORM_NAME}"
        )

    # =========================================================
    # VALIDAR INDEX
    # =========================================================

    if BS_DEVICE_INDEX < 0:

        raise ValueError(
            "BS_DEVICE_INDEX no puede ser negativo"
        )

    if BS_DEVICE_INDEX >= len(devices):

        raise ValueError(
            f"BS_DEVICE_INDEX={BS_DEVICE_INDEX} "
            f"no existe. "
            f"Hay {len(devices)} dispositivos configurados."
        )

    # =========================================================
    # DISPOSITIVO
    # =========================================================

    device = devices[
        BS_DEVICE_INDEX
    ]

    device_name = device[
        "name"
    ]

    platform_version = device[
        "platform_version"
    ]

    # =========================================================
    # LOG
    # =========================================================

    print("\n=================================")
    print("🌐 BROWSERSTACK")
    print("=================================")

    print(
        f"Device: {device_name}"
    )

    print(
        f"Platform: {platform}"
    )

    print(
        f"Version: {platform_version}"
    )

    print(
        f"Index: {BS_DEVICE_INDEX}"
    )

    print(
        f"App: {BS_APP}"
    )

    print(
        f"Local: {BS_LOCAL}"
    )

    print(
        f"Local Identifier: "
        f"{BS_LOCAL_IDENTIFIER}"
    )

    print("=================================\n")

    # =========================================================
    # ANDROID
    # =========================================================

    if platform == "android":

        options = UiAutomator2Options()

        options.load_capabilities({

            # -------------------------------------------------
            # APPIUM
            # -------------------------------------------------

            "platformName":
                "Android",

            "appium:deviceName":
                device_name,

            "appium:platformVersion":
                platform_version,

            "appium:automationName":
                "UiAutomator2",

            "appium:app":
                BS_APP,

            "appium:noReset":
                False,

            "appium:newCommandTimeout":
                120,

            # -------------------------------------------------
            # BROWSERSTACK OPTIONS
            # -------------------------------------------------

            "bstack:options": {

                "userName":
                    BS_USERNAME,

                "accessKey":
                    BS_ACCESS_KEY,

                "projectName":
                    "Mobile Automation",

                "buildName":
                    "Smoke",

                "sessionName":
                    f"Android - {device_name}",

                # -------------------------------------------------
                # LOCAL TESTING
                # -------------------------------------------------

                "local":
                    BS_LOCAL,

                "localIdentifier":
                    BS_LOCAL_IDENTIFIER,

                # -------------------------------------------------
                # LOGS
                # -------------------------------------------------

                "debug":
                    True,

                "networkLogs":
                    True,

                "deviceLogs":
                    True,

                "video":
                    True
            }
        })

    # =========================================================
    # IOS
    # =========================================================

    else:

        options = XCUITestOptions()

        options.load_capabilities({

            # -------------------------------------------------
            # APPIUM
            # -------------------------------------------------

            "platformName":
                "iOS",

            "appium:deviceName":
                device_name,

            "appium:platformVersion":
                platform_version,

            "appium:automationName":
                "XCUITest",

            "appium:app":
                BS_APP,

            "appium:noReset":
                False,

            "appium:newCommandTimeout":
                120,

            # -------------------------------------------------
            # BROWSERSTACK OPTIONS
            # -------------------------------------------------

            "bstack:options": {

                "userName":
                    BS_USERNAME,

                "accessKey":
                    BS_ACCESS_KEY,

                "projectName":
                    "Mobile Automation",

                "buildName":
                    "Smoke",

                "sessionName":
                    f"iOS - {device_name}",

                # -------------------------------------------------
                # LOCAL TESTING
                # -------------------------------------------------

                "local":
                    BS_LOCAL,

                "localIdentifier":
                    BS_LOCAL_IDENTIFIER,

                # -------------------------------------------------
                # LOGS
                # -------------------------------------------------

                "debug":
                    True,

                "networkLogs":
                    True,

                "deviceLogs":
                    True,

                "video":
                    True
            }
        })

    # =========================================================
    # BROWSERSTACK HUB
    # =========================================================

    command_executor = (
        "https://hub.browserstack.com/wd/hub"
    )

    # =========================================================
    # CREAR DRIVER
    # =========================================================

    driver = webdriver.Remote(
        command_executor=command_executor,
        options=options
    )

    return driver