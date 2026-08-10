class Queries:

    GET_USER = """
        SELECT USUARIO 
        FROM usuarios
        ORDER BY id_usuario;
    """

    GET_ACCOUNT = """
        SELECT * FROM cuentas
        WHERE ID_CUENTA = :id_cuenta;
    """

    