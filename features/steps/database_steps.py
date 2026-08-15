from behave import then
from database.queries import Queries


@then("deberían existir usuarios en la base de datos")
def step_verify_users(context):

    users = context.user_repository.get_users()

    print("\n👤 USUARIOS ENCONTRADOS:")
    print(users)

    context.db_evidence = {
        "query": Queries.GET_USER,
        "parameters": {},
        "result": users
    }

    assert users, "No existen usuarios en la base de datos"

@then('la cuenta con ID "{id_cuenta}" debería existir')
def verify_account(context, id_cuenta):

    account = context.account_repository.get_account(
        int(id_cuenta)
    )

    assert account is not None, (
        f"La cuenta con ID {id_cuenta} no existe."
    )

    

    print("\n💰 CUENTA ENCONTRADA:")
    print(account)

    context.db_evidence = {
                "query": Queries.GET_ACCOUNT,
                "parameters": {},
                "result": account
            }

from behave import then


@then("debería existir información de usuarios en la base de datos")
def step_verify_users_database(context):

    users = context.user_repository.get_users()

    print("\n👤 USUARIOS ENCONTRADOS:")
    print(users)

    assert users, (
        "No se encontraron usuarios "
        "en la base de datos"
    )