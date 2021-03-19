#!/usr/bin/env python
# encoding: utf-8

import ssl
import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError
from utils import config

conf = config.kafka_setting

context = ssl.create_default_context()
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = False
context.load_verify_locations(conf['ca_location'])

producer = KafkaProducer(bootstrap_servers=conf['bootstrap_servers'],
                        sasl_mechanism='PLAIN',
                        ssl_context=context,
                        security_protocol='SASL_SSL',
                        api_version = (0,10),
                        retries=5,
                        sasl_plain_username=conf['sasl_plain_username'],
                        sasl_plain_password=conf['sasl_plain_password'])

partitions = producer.partitions_for(conf['topic_name'])

timenow = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
try:
    future = producer.send(conf['topic_name'],  key=b'VehicleTelemetry', value=f'Test Data: {timenow}'.encode('utf-8'))
    future.get()
    print('send message succeed.')
except KafkaError as e:
    print('send message failed.', e)
