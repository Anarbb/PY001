import pika
import time
from pymongo import MongoClient

# MongoDB connection details
MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
MONGO_DB = 'usernames'
MONGO_USER = 'anas'
MONGO_PASS = 'asecretpassword'

def callback(ch, method, properties, body):
    username = body.decode()
    print(f"Received message: {username}")
    time.sleep(5)

    # Connect to MongoDB and save the username in the database
    client = MongoClient(MONGO_HOST, MONGO_PORT,
                         username=MONGO_USER, password=MONGO_PASS, authSource=MONGO_DB)
    db = client[MONGO_DB]
    if 'usernames' not in db.list_collection_names():
        db.create_collection('usernames')
    collection = db['usernames']
    collection.insert_one({'username': username})

    print(f"Username '{username}' stored in MongoDB")

    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='user_data')
    channel.basic_consume(queue='user_data', on_message_callback=callback)
    print('Waiting for messages...')

    channel.start_consuming()

if __name__ == "__main__":
    while True:
        try:
            consume_queue()
        except Exception as e:
            print(f"Error while consuming queue: {e}")
            time.sleep(5)
