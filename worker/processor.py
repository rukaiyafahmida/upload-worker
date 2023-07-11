from redis_function import RedisHandler
import re
from json import loads


redis_handler = RedisHandler()


def count_words_with_length(document, k):
    # Split the document content into words
    words = document.split()

    # Count the number of words with length k
    count = sum(1 for word in words if len(word) == k)

    return count



def count_words_with_length2(document, k):
    pattern = r'\b\w{' + str(k) + r'}\b'
    matches = re.findall(pattern, document)
    count = len(matches)
    return count


def process_document(message_json):
    message = loads(message_json)
    id = message['id']
    k = message['k']
    data  = message['data']
    try:
        count =  count_words_with_length(document=data, k=k)
    except Exception as e:
        #TODO
        pass
    if count:
        redis_handler.acknowledge(message=message_json)

    redis_handler.set_output(id=id, output=count)




def main():

    while True:
        message_json = redis_handler.dequeue()  # this blocks until an item is received
        process_document(message_json)


if __name__ == '__main__':
    main()