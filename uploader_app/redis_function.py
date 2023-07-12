import redis
import os
from dotenv import load_dotenv
from json import dumps

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_DB = int(os.getenv("REDIS_DB"))

PROCESSING_QUEUE = os.getenv("PROCESSING_QUEUE")


class RedisHandler:
    def __init__(self):
        """
        Initializes a RedisHandler object.

        The RedisHandler class provides methods to interact with a Redis server,
        including pushing messages to a processing queue, checking if a key exists,
        and retrieving output values associated with IDs.

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

    def enqueue(self, id, k, data):
        """
        Pushes a message to the processing queue.

        Args:
            id (str): The ID of the message.
            k (str): The key associated with the data.
            data (bytes): The data to be pushed to the queue.

        Raises:
            redis.exceptions.RedisError: If there is an error communicating with the Redis server.
        """
        msg = {"id": id, "k": k, "data": data.decode("utf-8")}
        self.client.rpush(self.queue_name, dumps(msg))

    def key_exists(self, id):
        """
        Checks if a key exists in Redis.

        Args:
            id (str): The ID of the key to check.

        Returns:
            bool: True if the key exists, False otherwise.

        Raises:
            redis.exceptions.RedisError: If there is an error communicating with the Redis server.
        """
        if self.client.exists(id) == 0:
            return False
        return True

    def get_output(self, id):
        """
        Retrieves the output value associated with an ID from Redis.

        Args:
            id (str): The ID to retrieve the output for.

        Returns:
            str: The output value associated with the ID, or None if the key doesn't exist.

        Raises:
            redis.exceptions.RedisError: If there is an error communicating with the Redis server.
        """
        output = self.client.get(name=id)
        return output
