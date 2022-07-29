
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.config import MONGO_URL, MONGO_DB_NAME

client = AsyncIOMotorClient(MONGO_URL)
engine = AIOEngine(motor_client=client, database=MONGO_DB_NAME)


class MongoDB:
    def __init__(self):
        self.client = None
        self.engine = None

    def connect(self):
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.engine = AIOEngine(motor_client=self.client, database=MONGO_DB_NAME)
        print("DB와 성공적으로 연결되었습니다")

    def close(self):
        print("DB를 종료합니다.")
        self.client.close()


mongodb = MongoDB()
