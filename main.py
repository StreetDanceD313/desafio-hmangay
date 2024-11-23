from fastapi import FastAPI
from pydantic import BaseModel
import redis
import pika
import pika.credentials
import json
from datetime import datetime

params = pika.URLParameters('amqp://teste:123456@localhost:5672/demo-vhost')
class RequestScrap(BaseModel):
    cnpj: str 

r = redis.Redis(host='localhost', port=6379, password='Redis2024', db=0)

app = FastAPI()


@app.get("/scrap/{cnpj}")
async def loop_for_scrap_in_redis(cnpj: str):
    data = r.get(cnpj)
    response = 'No data related do Cnpj Yet'
    if data != None :
        response = data
    return response

    
@app.post("/scrap")
async def add_scrap_to_rabbit_queue(item: RequestScrap):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare('scrap_cnpj')
    channel.queue_declare(queue="scrap", passive=True, durable=True)
    channel.queue_bind("scrap", "scrap_cnpj", "scrap")
    channel.basic_publish(exchange="scrap_cnpj",
                                routing_key="scrap",
                                body=item.cnpj)
    channel.close()
    connection.close()
    return True

