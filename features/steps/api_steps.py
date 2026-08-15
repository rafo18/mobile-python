from behave import when, then


@when('consulto el Pokemon "{pokemon}"')
def step_get_pokemon(context, pokemon):

    context.response = context.pokemon_api.get_pokemon(
        pokemon
    )

    print("\n🌐 RESPONSE:")
    print(context.response.json())


@then('la API debería responder con código {status_code:d}')
def step_verify_status_code(context, status_code):

    assert context.response.status_code == status_code


@then('el Pokemon debería llamarse "{pokemon}"')
def step_verify_pokemon_name(context, pokemon):

    data = context.response.json()

    assert data["name"] == pokemon


@then('el ID del Pokemon debería ser {pokemon_id:d}')
def step_verify_pokemon_id(context, pokemon_id):

    data = context.response.json()

    assert data["id"] == pokemon_id