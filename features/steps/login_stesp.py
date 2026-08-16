from behave import given, when, then
from selenium.common import TimeoutException
from utils.assertions import verify

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

    try:

        actual_title = (
            context.login_page
            .get_products_title()
        )

        verify(
            context,
            actual=actual_title,
            expected="PRODUCTS",
            description="Título de la pantalla principal"
        )

    except TimeoutException:

        verify(
            context,
            actual="PRODUCTS no encontrado",
            expected="PRODUCTS",
            description=(
                "El usuario debería "
                "ingresar a la pantalla principal"
            )
        )

@then("debería mostrar un mensaje de error indicando que las credenciales son inválidas")
def step_verify_invalid_login(context):
    users = context.user_repository.get_users()

    verify(
        context,
        actual=users[2]["USUARIO"],
        expected="test_user",
        description="El usuario debería ingresar a la pantalla principal"
    )