from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class LoginPage(BasePage):

    USERNAME = (
        AppiumBy.ACCESSIBILITY_ID,
        "test-Userna"
    )

    PASSWORD = (
        AppiumBy.ACCESSIBILITY_ID,
        "test-Password"
    )

    LOGIN_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "test-LOGIN"
    )

    def enter_username(self, username):
        self.enter_text(self.USERNAME, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)