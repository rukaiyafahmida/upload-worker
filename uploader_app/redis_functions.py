import redis
import os
from dotenv import load_dotenv
from json import dumps

load_dotenv()

REDIS_HOST= os.getenv("REDIS_HOST")
REDIS_PORT=int(os.getenv("REDIS_PORT"))
REDIS_DB=int(os.getenv("REDIS_DB"))

PROCESSING_QUEUE=os.getenv("PROCESSING_QUEUE")


class RedisHandler():
    def __init__(self):
        self.client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        queue_name=PROCESSING_QUEUE,
        decode_responses=True
    )
    def proccesing_queue_push(self, id, k, data):
        msg = {'id': id, 'k' : k, 'data': data}
        self.client.rpush(self.queue_name, dumps(msg))



