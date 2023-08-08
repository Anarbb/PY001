from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pika
from time import sleep

class User(BaseModel):
    username: str

app = FastAPI()

def send_message(message, rabbitmq_host):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
        channel = connection.channel()
        channel.queue_declare(queue='user_data')
        channel.basic_publish(exchange='', routing_key='user_data', body=message)
    except Exception as e:
        raise Exception("Failed to send message to RabbitMQ: " + str(e))
    finally:
        connection.close()

@app.post('/api/v1/adduser', status_code=201)
async def add_user(user: User):
    try:
        send_message(user.username, rabbitmq_host='rabbitmq')
        sleep(2)
        return {'username': user.username + ' added successfully'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
