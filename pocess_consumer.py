# -*- coding: utf-8 -*
import pika
import sys
from db import Db
import time
from multiprocessing import Process, Pool
import os
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


def run_proc(name):        ##定义一个函数用于进程调用
    for i in range(5):
        channel.start_consuming()
#执行一次该函数共需1秒的时间

if __name__ =='__main__': #执行主进程
    mainStart = time.time() #记录主进程开始的时间
    p = Pool(4)           #开辟进程池
    for i in range(16):                                 #开辟14个进程
        p.apply_async(run_proc,args=('Process'+str(i),))#每个进程都调用run_proc函数，
                                                        #args表示给该函数传递的参数。
    p.close() #关闭进程池
    p.join()  #等待开辟的所有进程执行完后，主进程才继续往下执行





