@smoke
Feature: Integración Front API y Base de Datos

    @api @database
    Scenario: Validar usuario desde Front, API y Base de Datos

        Given que el usuario abre la aplicación
        When ingresa el usuario "standard_user"
        And ingresa la contraseña "secret_sauce"
        And presiona el botón LOGIN
        And consulto el Pokemon "pikachu"
        Then la API debería responder con código 200
        And el Pokemon debería llamarse "pikachu"
        And debería existir información de usuarios en la base de datos
        And debería ingresar correctamente a la aplicación