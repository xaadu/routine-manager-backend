from typing import List
from .dbmanager import DatabaseManager


class CourseDatabaseManager(DatabaseManager):
    def __init__(self) -> None:
        super().__init__()

        self.courses = self.db.courses

    async def get_courses(self) -> List[dict]:
        res = await self.courses.find({}, {"_id": 0}).to_list(1000)
        return res

    async def insert_course(self, data: dict) -> dict:
        res = await self.courses.insert_one(data)
        res = await self.courses.find_one({"_id": res.inserted_id}, {"_id": 0})
        return res
    
    async def remove_course(self, course_code:str) -> int:
        res = await self.courses.delete_one({"course_code": course_code})
        return res.deleted_count
