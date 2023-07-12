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
        decode_responses=True)
        self.queue_name=PROCESSING_QUEUE
        
    def proccesing_queue_push(self, id, k, data):
        msg = {'id': id, 'k' : k, 'data': data.decode('utf-8')}
        self.client.rpush(self.queue_name, dumps(msg))
    
    def key_exists(self, id):
        if self.client.exists(id) == 0:
            return False
        return True

    def get_output(self, id):
        output = self.client.get(name=id)
        return output
    


