from database.connection import DatabaseConnection
from database.queries import Queries


db = DatabaseConnection()

try:

    db.connect()

    print("\n✅ BASE DE DATOS CONECTADA")

    result = db.execute_query(
        Queries.GET_USER 
    )

    print("\nResultado:")
    print(result)

    result2 = db.execute_query(
        Queries.GET_ACCOUNT,
        {"id_cuenta": 4}
    )

    print("\nResultado2:")
    print(result2)
finally:

    db.close()