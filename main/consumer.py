import pika, json
from weatherAnalysis import weatherGetter

from main import Prediction, db

params = pika.URLParameters('amqps://kwbvjvnw:ZLVHOXhkRMBOIvCw26A1Lu6srlXaiZYQ@hawk.rmq.cloudamqp.com/kwbvjvnw')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'prediction_created':
        prediction = Prediction(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(prediction)
        db.session.commit()
        print('Prediction Created')

    elif properties.content_type == 'prediction_updated':
        prediction = Prediction.query.get(data['id'])
        prediction.title = data['title']
        prediction.image = weatherGetter(data['title'])
        db.session.commit()
        print('Prediction Updated')

    elif properties.content_type == 'prediction_deleted':
        prediction = Prediction.query.get(data)
        db.session.delete(prediction)
        db.session.commit()
        print('Prediction Deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
