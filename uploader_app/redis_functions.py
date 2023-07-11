import redis
import os
from dotenv import load_dotenv
from json import dumps

load_dotenv()

REDIS_HOST= os.getenv("REDIS_HOST")
REDIS_PORT=int(os.getenv("REDIS_PORT"))
REDIS_DB=int(os.getenv("REDIS_DB"))

PROCESSING_QUEUE=os.getenv("PROCESSING_QUEUE")
COMPLETED_QUEUE=os.getenv("COMPLETED_QUEUE")


class RedisHandler():
    def __init__(self):
        self.client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True
    )
    def add_to_proccesing(self, id, k, data):
        msg = {'id': id, 'k' : k, 'data': data}
        self.client.rpush(PROCESSING_QUEUE, dumps(msg))



