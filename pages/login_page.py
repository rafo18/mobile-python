from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class LoginPage:

    USERNAME = (AppiumBy.ACCESSIBILITY_ID, "test-Username")
    PASSWORD = (AppiumBy.ACCESSIBILITY_ID, "test-Password")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")

    def __init__(self, driver):
        self.driver = driver

    def enter_username(self, username):
        element = self.driver.find_element(*self.USERNAME)
        element.clear()
        element.send_keys(username)

    def enter_password(self, password):
        element = self.driver.find_element(*self.PASSWORD)
        element.clear()
        element.send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()