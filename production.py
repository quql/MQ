# -*- coding: utf-8 -*-
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#创建队列。有就不管，没有就自动创建
channel.queue_declare(queue='hello')

#使用默认的交换机发送消息。exchange为空就使用默认的
channel.basic_publish(exchange='', routing_key='hello', body='Hello World123456!')
print(" [x] Sent 'Hello World!'")
connection.close()