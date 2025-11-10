import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ[
    "OPENAI_API_KEY"] = ""


async def function_one():

    openai_model_client = OpenAIChatCompletionClient(
        model="gpt-4o"
    )
    assistant = AssistantAgent(name="Assistant", model_client=openai_model_client)
    await Console(assistant.run_stream(task="What do you mean by yankee?")) #run_stream gives the output in the console line by line. But run will just give you a cumulative result at the end.
    await openai_model_client.close()


asyncio.run(function_one())
