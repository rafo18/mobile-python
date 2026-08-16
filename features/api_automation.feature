Feature: API Automation

    @api
    Scenario: Crear un post mediante API

        When envío una petición POST para crear un post
        Then la API debería responder con código 201
        And el post creado debería tener el título "Mobile Automation"