import motor.motor_asyncio

from vars import MONGODB_CONNECTION_STRING, MONGODB_DB


class DatabaseManager:
    def __init__(self) -> None:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
        self.db = client.get_database(MONGODB_DB)
