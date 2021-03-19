'''
Author:     Jixin Jia (Gin)
Date:       03/18
Purpose:    For use with Function Compute to generate simulated engine sensor data.
            Markov-chain is used to alternate between irregular and normal engine behaviors. 
'''
from markov_chain import MarkovChain
from kafka import KafkaProducer
from kafka.errors import KafkaError
from utils import config
from utils import routes
import time
import numpy as np
import random
import datetime
import json
import ssl
import logging


def handler(event, context):
    # init
    conf = config.kafka_setting
    logger = logging.getLogger()

    # event counter
    event_count = 0

    # Create a Kafka producer client to send messages to the Kafka
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

    # define Markov Chain status shift probability
    MK_TRANSITION_PROB = {
        'Normal': {'Normal': 0.9, 'Abnormal': 0.1},
        'Abnormal': {'Normal': 0.5, 'Abnormal': 0.5}
        }

    mk_chain = MarkovChain(transition_prob=MK_TRANSITION_PROB)
    current_state = False

    # randomly selects a route
    coords = random.choice(routes.routes)

    # reset status in MK chain
    if not current_state:
        current_state = 'Normal'

    for coord in coords:
        lng = coord[0]
        lat = coord[1]
        
        # generate telemetry
        current_state = mk_chain.generate_states(current_state=current_state, no=1)[0]
        skewness = 2+random.random() if current_state == 'Abnormal' else 1
        payload = {
            'timestamp': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            'vin': 'PAI-Vehicle',
            'lat': lat,
            'long':  lng,
            'rpm': int(np.random.chisquare(df=10, size=1)*1000 * skewness),
            'coolant_temp': round(float(np.random.uniform(low=70, high=90, size=1)) * skewness,1),
            'vapor_pressure': round(float(np.random.uniform(low=6000, high=8000, size=1)) * skewness,1),
            'cm_voltage':int(int(np.random.chisquare(df=2, size=1)*100) * skewness),
            'torque_percent':round(float(np.random.normal(loc=50, scale=10, size=1)) * skewness,1),
            'oxygen_rate': round(float(np.random.normal(loc=80, scale=20, size=1)) * skewness,1)
        }
        
        # Send telemetry to Kafka
        try:
            future = producer.send(conf['topic_name'],  json.dumps(payload).encode('utf-8'))
            future.get()
            logger.info('Success: ', json.dumps(payload))
        except KafkaError as e:
            logger.error('Failure', e)
            break
        
        event_count += 1

        if event_count >= 10:
            break
        else:            
            # idle for 5 seconds
            time.sleep(5)
    
    return f'Sent {event_count} messages'
