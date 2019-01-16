#!/usr/bin/env python
import pika
from tkinter import messagebox

credits = pika.PlainCredentials('india','india')
params = pika.ConnectionParameters('10.10.0.222',5672,'/',credits)
connection = pika.BlockingConnection(parameters=params)
channel = connection.channel()


channel.queue_declare(queue='in_error_queue', durable=True)

def callback(ch, method, properties, body):
    messagebox.showinfo("MQ Lisner", body)
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='in_error_queue',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()