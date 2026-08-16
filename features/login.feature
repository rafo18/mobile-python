@smoke
Feature: Login

  Scenario: Login exitoso con credenciales válidas
    Given que el usuario abre la aplicación
    When ingresa el usuario "standard_user"
    And ingresa la contraseña "secret_sauce"
    And presiona el botón LOGIN
    Then debería ingresar correctamente a la aplicación

@database
  Scenario: Login fallido con credenciales inválidas
    Given que el usuario abre la aplicación
    When ingresa el usuario "invalid_user"
    And ingresa la contraseña "invalid_password"
    And presiona el botón LOGIN
    Then debería mostrar un mensaje de error indicando que las credenciales son inválidas