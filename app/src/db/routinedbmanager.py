from .dbmanager import DatabaseManager


class RoutineDatabaseManager(DatabaseManager):
    def __init__(self) -> None:
        super().__init__()

        self.routines = self.db.routines

    async def add_routine(self, data: dict) -> dict:
        res = await self.routines.insert_one(data)
        return res
