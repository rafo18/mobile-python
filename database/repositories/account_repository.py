from database.queries import Queries


class AccountRepository:

    def __init__(self, db):
        self.db = db

    def get_account(self, id_cuenta):

        return self.db.execute_query_one(
            Queries.GET_ACCOUNT,
            {
                "id_cuenta": id_cuenta
            }
        )