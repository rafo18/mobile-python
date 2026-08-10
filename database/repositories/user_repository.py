from database.queries import Queries


class UserRepository:

    def __init__(self, db):
        self.db = db

    def get_users(self):
        return self.db.execute_query(
            Queries.GET_USER
        )
    