import pika, json

params = pika.URLParameters('amqps://kwbvjvnw:ZLVHOXhkRMBOIvCw26A1Lu6srlXaiZYQ@hawk.rmq.cloudamqp.com/kwbvjvnw')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
