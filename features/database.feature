@database
Feature: Validaciones de base de datos

  
  Scenario: Consultar usuarios registrados

    Then deberían existir usuarios en la base de datos

  
  Scenario: Consultar una cuenta

    Then la cuenta con ID "1" debería existir

  Scenario: update cuenta

    When actualizo la cuenta con ID "1" con saldo "5000"
    Then la cuenta con ID "1" debería tener saldo "5000"