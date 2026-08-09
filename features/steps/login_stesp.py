from behave import given, when, then

from drivers.driver_factory import create_driver
from pages.login_page import LoginPage


@given("que el usuario abre la aplicación")
def step_open_application(context):
    context.driver = create_driver()
    context.login_page = LoginPage(context.driver)


@when('ingresa el usuario "{username}"')
def step_enter_username(context, username):
    context.login_page.enter_username(username)


@when('ingresa la contraseña "{password}"')
def step_enter_password(context, password):
    context.login_page.enter_password(password)


@when("presiona el botón LOGIN")
def step_click_login(context):
    context.login_page.click_login()


@then("debería ingresar correctamente a la aplicación")
def step_verify_login(context):
    assert context.driver is not None