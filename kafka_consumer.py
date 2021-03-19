#!/usr/bin/env python
# encoding: utf-8

import ssl
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from utils import config

conf = config.kafka_setting


context = ssl.create_default_context()
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = False
context.load_verify_locations(conf['ca_location'])

consumer = KafkaConsumer(bootstrap_servers=conf['bootstrap_servers'],
                        group_id=conf['consumer_id'],
                        api_version = (0,10,2),
                        session_timeout_ms=25000,
                        max_poll_records=100,
                        fetch_max_bytes=1 * 1024 * 1024,
                        security_protocol='SASL_SSL',
                        sasl_mechanism="PLAIN",
                        ssl_context=context,
                        sasl_plain_username=conf['sasl_plain_username'],
                        sasl_plain_password=conf['sasl_plain_password'])

print('consumer start to consuming...')
consumer.subscribe((conf['topic_name'], ))
for message in consumer:
    print(f'Topic: {message.topic}, Offset: {message.offset}, Key: {message.key}, Value: {message.value}, Partition: {message.partition}')
