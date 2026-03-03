from kafka import KafkaProducer
from loguru import logger
from time import sleep
import json

from producer_utils.data_reader import get_data


def producer_execute():
    logger.add('./producer.log')
    producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: v.encode('utf-8'))
    datas = get_data('mock_data/client_data.csv')
    logger.info('Start sending message to Kafka...')
    for data in datas:
        data_str = json.dumps(data)
        producer.send(topic='insurance', value=data_str)
        logger.info(f'SENDING: || {data_str}')
        sleep(3)


if __name__ == '__main__':
    producer_execute()
