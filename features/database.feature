Feature: Validaciones de base de datos

  @database
  Scenario: Consultar usuarios registrados

    Then deberían existir usuarios en la base de datos

  @database
  Scenario: Consultar una cuenta

    Then la cuenta con ID "1" debería existir