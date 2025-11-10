import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ[
    "OPENAI_API_KEY"] = ""


async def function_one():

    openai_model_client = OpenAIChatCompletionClient(
        model="gpt-4o"
    )
    agent1 = AssistantAgent(name="MathsAgent", model_client=openai_model_client, system_message="You are a mathematics teacher. So please respond like a teacher.")

    agent2 = AssistantAgent(name="Student", model_client=openai_model_client, system_message="You are a curious student teacher. So please behave like a student.")

    team = RoundRobinGroupChat(participants=[agent1, agent2], termination_condition=MaxMessageTermination(max_messages=6))

    await Console(team.run_stream(
        task="Lets discuss how calculus works"))  # run_stream gives the output in the console line by line. But run will just give you a cumulative result at the end.
    await openai_model_client.close()


asyncio.run(function_one())
