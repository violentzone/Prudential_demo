from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
import asyncio
from .llm_agents import *


consumer_pipeline_agent = SequentialAgent(name='ConsumerPipelineAgent', description="Take Kafka consumer's message and process with different agent group", sub_agents=[decide_agent, calculate_fee_agent, summary_agent])

