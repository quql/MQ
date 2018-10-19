# -*- coding: utf-8 -*-
import pika
import sys
import requests
credentials = pika.PlainCredentials("qql", "123456")
parameters = pika.ConnectionParameters(host="192.168.81.109", 
                                                virtual_host='/', 
                                                credentials=credentials)
connection = pika.BlockingConnection(parameters)    # 连接 RabbitMQ
channel = connection.channel()

# rabbitmq消费端仍然使用此方法创建队列。这样做的意思是：若是没有就创建。和发送端道理道理。目的是为了保证队列一定会有
channel.queue_declare(durable=True,queue='qql')
#绑定交换机队列
channel.queue_bind(exchange='msg', queue='qql',routing_key='qql') 
# 收到消息后的回调
def callback(ch, method, properties, body):
    url = 'http://192.168.81.109';
    response = requests.post(url, data=body)
    print response

channel.basic_consume(callback,queue='qql',no_ack=True)

print ' [*] Waiting for messages. To exit press CTRL+C'
channel.start_consuming()
