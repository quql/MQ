# -*- coding: utf-8 -*
from flask import Flask,request
import pika,json
app = Flask(__name__)
@app.route("/",methods = ['GET', 'POST'])
def index():
    if request.method == "POST":
        data = request.data
        return sendmqueue(data)
    if request.method == "GET":
        return ('<h1>HELLO WORLD!!</h1>')

def sendmqueue(que):
    credentials = pika.PlainCredentials("qql", "123456")
    parameters = pika.ConnectionParameters(host="192.168.81.109", 
                                                virtual_host='/', 
                                                credentials=credentials)
    connection = pika.BlockingConnection(parameters)    # 连接 RabbitMQ
    channel = connection.channel()

    #创建队列。有就不管，没有就自动创建
    channel.queue_declare(queue='qql',durable=True)

    #使用默认的交换机发送消息。exchange为空就使用默认的
    res=channel.basic_publish(exchange='msg', routing_key='qql', body=que)
    connection.close()
    if res==True:
        return ('true')
    else:
        return ('false')        
    

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=7777,
        debug=True
    )