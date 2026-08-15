Feature: Consultas a PokeAPI
  @api
  Scenario: Consultar Pikachu
    When consulto el Pokemon "pikachu"
    Then la API debería responder con código 200
    And el Pokemon debería llamarse "pikachu"
    And el ID del Pokemon debería ser 896