from .dbmanager import DatabaseManager


class LecturersDatabaseManager(DatabaseManager):
    def __init__(self) -> None:
        super().__init__()

        self.lecturers = self.db.lecturers

    async def get_lecturers(self) -> list:
        res = await self.lecturers.find({}, {"_id": 0}).to_list(100)
        return res

    async def insert_lecturer(self, data: dict) -> dict:
        res = await self.lecturers.insert_one(data)
        res = await self.lecturers.find_one({"_id": res.inserted_id}, {"_id": 0})
        return res
    
    async def remove_lecturer(self, lecturer_code:str) -> int:
        res = await self.lecturers.delete_one({"code": lecturer_code})
        return res.deleted_count
