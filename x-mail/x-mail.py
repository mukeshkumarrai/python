#!/usr/bin/env python
import pika
import sys
import json
from tkinter import messagebox
import sendMail

with open('config.json') as conf_data:
        conf =  json.load(conf_data)
        mq_url             = conf['mq_url']
        mq_port            = conf['mq_port']
        mq_user            = conf['mq_user']
        mq_pass            = conf['mq_pass']

credits = pika.PlainCredentials(mq_user,mq_pass)
params = pika.ConnectionParameters(mq_url,mq_port,'/',credits)
connection = pika.BlockingConnection(parameters=params)
channel = connection.channel()



def callback(ch, method, properties, body):
    data = json.loads(body)
    Mail = sendMail.Smpt(data['server_host'], data['server_port'],data['hotel_id'],data['user_id'])
    smtpconf = Mail.connectsmtp(data['server_host'], data['server_port'],'', data['password'])
    qr_code = data['qr_code']
    if qr_code:
            # messagebox.showinfo("enter QR Code", data['subject'])
            Mail.qrcode(smtpconf,data['qr_code'],data['mail_from'],data['receipents'],data['subject'])
            print("QR Code ")
            
    else:
        Mail.plainmail(smtpconf,data['html_body'],data['mail_from'],data['receipents'],data['subject'])
        print("Normal Mail")

channel.basic_consume(callback,
                      queue='in_email_queue',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()