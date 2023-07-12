from redis_function import RedisHandler
from json import loads


redis_handler = RedisHandler()


def count_words_with_length(document, k):
    """
    Counts the number of words in a document with a specified length.

    Args:
        document (str): The document content.
        k (int): The desired word length.

    Returns:
        int: The count of words with length k in the document.

    Note:
        - Words are separated by whitespace.
        - Punctuation marks are considered part of a word.

    """

    # Split the document content into words
    words = document.split()

    # Count the number of words with length k
    count = sum(1 for word in words if len(word) == k)

    return count


def process_document(message_json):
    """
    Processes a document message in JSON format.

    The function takes a message in JSON format, extracts the necessary information,
    and performs word count processing on the document data. The word count is
    performed by calling the `count_words_with_length` function.

    Args:
        message_json (str): The document message in JSON format.
    """
    message = loads(message_json)
    id = message["id"]
    k = message["k"]
    data = message["data"]
    try:
        count = count_words_with_length(document=data, k=k)
    except Exception as e:
        print(f"Error occured while processing. Error: {e}", flush=True)
    if count:
        redis_handler.acknowledge(message=message_json)

    redis_handler.set_output(id=id, output=count)


def main():
    while True:
        message_json = redis_handler.dequeue()
        if message_json:
            process_document(message_json)


if __name__ == "__main__":
    main()
