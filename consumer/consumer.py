import time

from aiokafka import AIOKafkaConsumer
import asyncio
from loguru import logger
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import os
import dotenv
import json
from datetime import datetime

from agents.orchestrate_agent import consumer_pipeline_agent


dotenv.load_dotenv()


async def consume():
    logger.add('consumer.log')
    logger.info(f"""
    ╔══════════════════════════════════╗
    ║   🚀  CONSUMER STARTED           ║
    ║   Time   : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}   ║
    ╚══════════════════════════════════╝
    """)
    logger.info('Creating response folder...')
    os.makedirs('response', exist_ok=True)
    logger.info('CREATED')

    # Start runner
    session_service = InMemorySessionService()
    runner = Runner(agent=consumer_pipeline_agent, app_name='consumer_app_runner', session_service=session_service, auto_create_session=True)
    consumer = AIOKafkaConsumer("insurance", bootstrap_servers="kafka:9092")
    async with consumer:
        logger.info('Kafka consumer started')
        num_count = 1
        async for msg in consumer:
            for attempts in range(3):
                logger.info(f'Running respond generation {str(num_count)} attempt(s)')
                try:
                    content = types.Content(role='user', parts=[types.Part(text='Client information: ' + msg.value.decode('utf-8'))])
                    final_response_text = "Agent did not produce a final response."
                    async for event in runner.run_async(user_id='system', session_id='test', new_message=content):
                        if event.is_final_response():
                            if event.content and event.content.parts:
                                final_response_text = event.content.parts[0]
                                logger.info(f'Response acquired, generating .txt file in response/{num_count}.txt')
                                with open(f'response/{num_count}.txt', 'w', encoding='utf-8-sig') as f:
                                    f.write(final_response_text.text)

                    break
                except Exception as e:
                    logger.error(f'Error occur during calling Gemini API, {str(e)}')
                    time.sleep(.5)

            num_count += 1
            continue

if __name__ == '__main__':
    asyncio.run(consume())
