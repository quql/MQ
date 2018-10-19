# -*- coding: utf-8 -*
import pika
import sys
from db import Db
import time
# import requests
import json
credentials = pika.PlainCredentials('qql', '123456')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.233.130',5672,'message',credentials))
channel = connection.channel()

channel.exchange_declare(exchange='exchange_msg',
                         exchange_type='direct', 
                         durable=True)

try:
    channel.queue_declare(queue='send_msg', durable=True)
except:
    channel = connection.channel()
    channel.queue_delete(queue='send_msg')
    channel.queue_declare(queue='send_msg', durable=True)
# queue_name = result.method.queue
# 获取运行脚本所有的参数
severities = sys.argv[1:]
# if not severities:
#     sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
#     sys.exit(1)
# 循环列表去绑定
for severity in severities:
    channel.queue_bind(exchange='exchange_msg',
                       queue='send_msg',
                       routing_key='qql')

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    # url = 'https://www.qqlong.top/sendceshi'
    datas = json.loads(body)
    # post_data={'num':datas['num'],'key':datas['key']}
    # response = requests.post(url, data=datas)
    # res = response.json()
    Db().table('get_msg').insert({"msg":datas})
    time.sleep(5)
    print(datas)

channel.basic_consume(callback,
                      queue='send_msg',
                      no_ack=True)

channel.start_consuming()