from drivers.driver_factory import create_driver
from pages.login_page import LoginPage


driver = create_driver()

login_page = LoginPage(driver)

print("Aplicación abierta")

login_page.enter_username("standard_user")
login_page.enter_password("secret_sauce")

print("Credenciales ingresadas")

login_page.click_login()

print("Login ejecutado")

input("Presiona ENTER para cerrar...")

driver.quit()