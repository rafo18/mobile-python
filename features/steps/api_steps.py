from behave import when, then

from utils.assertions import verify


# =========================================================
# GET POKEMON
# =========================================================

@when('consulto el Pokemon "{pokemon}"')
def step_get_pokemon(context, pokemon):

    context.response = (
        context.pokemon_api.get_pokemon(
            pokemon
        )
    )

    print("\n🌐 API RESPONSE:")

    print(
        context.response.text
    )


# =========================================================
# STATUS CODE
# =========================================================

@then(
    'la API debería responder con código {status_code:d}'
)
def step_verify_status_code(
    context,
    status_code
):

    response = getattr(
        context,
        "api_response",
        None
    )

    if response is None:

        response = getattr(
            context,
            "response",
            None
        )

    if response is None:

        raise AssertionError(
            "No existe una respuesta API "
            "disponible."
        )

    verify(
        context,
        actual=response.status_code,
        expected=status_code,
        description="API Status Code"
    )


# =========================================================
# POKEMON NAME
# =========================================================

@then(
    'el Pokemon debería llamarse "{pokemon}"'
)
def step_verify_pokemon_name(
    context,
    pokemon
):

    data = (
        context.response.json()
    )

    verify(
        context,
        actual=data["name"],
        expected=pokemon,
        description="Pokemon Name"
    )


# =========================================================
# POKEMON ID
# =========================================================

@then(
    'el ID del Pokemon debería ser {pokemon_id:d}'
)
def step_verify_pokemon_id(
    context,
    pokemon_id
):

    data = (
        context.response.json()
    )

    verify(
        context,
        actual=data["id"],
        expected=pokemon_id,
        description="Pokemon ID"
    )


# =========================================================
# POST
# =========================================================

@when(
    "envío una petición POST para crear un post"
)
def step_create_post(context):

    body = {

        "title":
            "Mobile Automation",

        "body":
            "Prueba automatizada con Python",

        "userId":
            1
    }

    headers = {

        "Content-Type":
            "application/json",

        "Accept":
            "application/json"
    }

    context.api_response = (
        context.test_api.create_post(
            body=body,
            headers=headers
        )
    )

    print(
        "\n🌐 POST RESPONSE:"
    )

    print(
        context.api_response.text
    )


# =========================================================
# POST TITLE
# =========================================================

@then(
    'el post creado debería tener el título "{title}"'
)
def step_verify_post_title(
    context,
    title
):

    data = (
        context.api_response.json()
    )

    verify(
        context,
        actual=data["title"],
        expected=title,
        description="Post Title"
    )