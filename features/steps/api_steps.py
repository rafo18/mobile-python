from behave import when, then

from utils.assertions import verify


@when('consulto el Pokemon "{pokemon}"')
def step_get_pokemon(context, pokemon):

    endpoint = f"/pokemon/{pokemon}"

    context.response = context.pokemon_api.get_pokemon(
        pokemon
    )

    # =========================================================
    # API EVIDENCE
    # =========================================================

    try:
        response_data = context.response.json()
    except Exception:
        response_data = context.response.text

    context.api_evidence = {

        "method": "GET",

        "endpoint": (
            f"https://pokeapi.co/api/v2"
            f"{endpoint}"
        ),

        "parameters": {},

        "status_code": context.response.status_code,

        "response": response_data
    }

    print("\n🌐 API RESPONSE:")
    print(response_data)


@then('la API debería responder con código {status_code:d}')
def step_verify_status_code(context, status_code):

    verify(
        context,
        actual=context.response.status_code,
        expected=status_code,
        description="API Status Code"
    )


@then('el Pokemon debería llamarse "{pokemon}"')
def step_verify_pokemon_name(context, pokemon):

    data = context.response.json()

    verify(
        context,
        actual=data["name"],
        expected=pokemon,
        description="Pokemon Name"
    )


@then('el ID del Pokemon debería ser {pokemon_id:d}')
def step_verify_pokemon_id(context, pokemon_id):

    data = context.response.json()

    verify(
        context,
        actual=data["id"],
        expected=pokemon_id,
        description="Pokemon ID"
    )