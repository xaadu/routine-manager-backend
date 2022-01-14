from .dbmanager import DatabaseManager


class UserDatabaseManager(DatabaseManager):
    def __init__(self) -> None:
        super().__init__()

        # Collections
        self.users = self.db.users

        # Local Connection for not calling every request
        self.num_of_user = self.users.count_documents({})
