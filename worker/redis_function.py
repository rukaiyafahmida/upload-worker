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
COMPLETED_KEY_EXPIRATION= int(os.getenv("COMPLETED_KEY_EXPIRATION"))

class RedisHandler():
    def __init__(self):
        self.client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        queue_name = PROCESSING_QUEUE,
        decode_responses=True
    )
        
    def enqueue(self, message):
        self.client.rpush(self.queue_name, message)

    def dequeue(self):
        message = self.client.lmove(self.queue_name, self.queue_name, src='LEFT',dest='RIGHT')
        return message

    def acknowledge(self, message):
        self.client.lrem(self.queue_name, 0, message)
    
    def set_output(self, id, output):
        self.client.set(name=id, value=output)

    def get_output(self, id):
        output = self.client.get(name=id)
        return output


