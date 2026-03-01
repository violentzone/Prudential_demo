from aiokafka import AIOKafkaConsumer
import asyncio
from loguru import logger


async def consume():
    logger.add('consumer.log')
    logger.info('Consumer started ')
    consumer = AIOKafkaConsumer("insurance", bootstrap_servers="localhost:9092")
    await consumer.start()
    async for msg in consumer:
        print(msg)


if __name__ == '__main__':
    asyncio.run(consume())
