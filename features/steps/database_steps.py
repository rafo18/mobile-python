from behave import then


@then("deberían existir usuarios en la base de datos")
def verify_users(context):

    users = context.user_repository.get_users()

    assert users, (
        "No existen usuarios registrados en la base de datos."
    )

    print("\n👤 USUARIOS ENCONTRADOS:")

    for user in users:
        print(f"   - {user['USUARIO']}")


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