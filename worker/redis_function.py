import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_DB = int(os.getenv("REDIS_DB"))

PROCESSING_QUEUE = os.getenv("PROCESSING_QUEUE")
EXPIRATION_FOR_OUTPUT = int(os.getenv("EXPIRATION_FOR_OUTPUT"))


class RedisHandler:
    def __init__(self):
        """
        Initializes a RedisHandler object.

        The RedisHandler class provides methods to interact with a Redis server,
        including enqueueing and dequeueing messages, acknowledging processed messages,
        and setting output values associated with IDs.

        The Redis connection details are obtained from the following environment variables:
        - REDIS_HOST: Redis server hostname or IP address.
        - REDIS_PORT: Redis server port.
        - REDIS_DB: Redis database index to use.

        The processing queue name is set to PROCESSING_QUEUE.

        Raises:
            redis.exceptions.RedisError: If there is an error connecting to the Redis server.
        """
        self.client = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
        )
        self.queue_name = PROCESSING_QUEUE

    def enqueue(self, message):
        """
        Enqueues a message into the processing queue.

        Args:
            message (str): The message to enqueue.

        Raises:
            redis.exceptions.RedisError: If there is an error communicating with the Redis server.
        """
        self.client.rpush(self.queue_name, message)

    def dequeue(self):
        """
        Dequeues a message from the processing queue.

        Returns:
            str: The dequeued message.

        Raises:
            redis.exceptions.RedisError: If there is an error communicating with the Redis server.
        """
        message = self.client.lmove(
            self.queue_name, self.queue_name, src="LEFT", dest="RIGHT"
        )
        return message

    def acknowledge(self, message):
        """
        Acknowledges a processed message and removes it from the processing queue.

        Args:
            message (str): The message to acknowledge and remove.

        Raises:
            redis.exceptions.RedisError: If there is an error communicating with the Redis server.
        """
        self.client.lrem(self.queue_name, 0, message)

    def set_output(self, id, output):
        """
        Sets the output value associated with an ID and a expiration in Redis.

        Args:
            id (str): The ID to set the output for.
            output (str): The output value to set.

        Raises:
            redis.exceptions.RedisError: If there is an error communicating with the Redis server.
        """
        self.client.set(name=id, value=output)
        self.client.expire(name=id, time=EXPIRATION_FOR_OUTPUT)
