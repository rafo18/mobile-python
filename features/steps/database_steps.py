from behave import then, when
from database.queries import Queries
from utils.assertions import verify



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
@when('actualizo la cuenta con ID "{id_cuenta}" con saldo "{saldo}"')
def step_update_account(context, id_cuenta, saldo):

    context.account_repository.update_account(
        id_cuenta=id_cuenta,
        saldo=saldo
    )

    print(f"\n💰 CUENTA CON ID {id_cuenta} ACTUALIZADA CON SALDO {saldo}")

@then('la cuenta con ID "{id_cuenta}" debería tener saldo "{saldo}"')
def step_verify_account_balance(context, id_cuenta, saldo):

    account = context.account_repository.get_account(
        id_cuenta=id_cuenta
    )

    verify(
    context,
    actual=float(account["SALDO"]),
    expected=float(saldo),
    description=f"Saldo de la cuenta con ID {id_cuenta}"
    )