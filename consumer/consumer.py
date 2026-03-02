from aiokafka import AIOKafkaConsumer
import asyncio
from loguru import logger
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import os

from agents.orchestrate_agent import consumer_pipeline_agent


async def consume():
    logger.add('consumer.log')
    logger.info('Consumer started ')
    os.makedirs('response', exist_ok=True)

    # Start runner
    session_service = InMemorySessionService()
    runner = Runner(agent=consumer_pipeline_agent, app_name='consumer_app_runner', session_service=session_service, auto_create_session=True)
    consumer = AIOKafkaConsumer("insurance", bootstrap_servers="localhost:9092")
    await consumer.start()

    num_count = 1
    async for msg in consumer:
        content = types.Content(role='user', parts=[types.Part(text=msg)])
        final_response_text = "Agent did not produce a final response."
        print(msg)
        async for event in runner.run_async(user_id='system', session_id='test', new_message=content):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0]
                    with open(f'response/{num_count}') as f:
                        f.write(final_response_text.text)

                break
        num_count += 1

if __name__ == '__main__':
    asyncio.run(consume())
