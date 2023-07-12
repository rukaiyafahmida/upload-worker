import redis
import os
from dotenv import load_dotenv
from json import dumps

load_dotenv()

REDIS_HOST= os.getenv("REDIS_HOST")
REDIS_PORT=int(os.getenv("REDIS_PORT"))
REDIS_DB=int(os.getenv("REDIS_DB"))

PROCESSING_QUEUE=os.getenv("PROCESSING_QUEUE")
EXPIRATION_FOR_OUTPUT=int(os.getenv("EXPIRATION_FOR_OUTPUT"))

class RedisHandler():
    def __init__(self):
        self.client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True)
        self.queue_name=PROCESSING_QUEUE
        
    def enqueue(self, message):
        self.client.rpush(self.queue_name, message)

    def dequeue(self):
        message = self.client.lmove(self.queue_name, self.queue_name, src='LEFT',dest='RIGHT')
        return message

    def acknowledge(self, message):
        self.client.lrem(self.queue_name, 0, message)
    
    def set_output(self, id, output):
        self.client.set(name=id, value=output)
        self.client.expire(name=id,time=EXPIRATION_FOR_OUTPUT)


