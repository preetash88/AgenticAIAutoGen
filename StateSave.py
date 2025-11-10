import asyncio
import json
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ[
    "OPENAI_API_KEY"] = ""


async def function_one():
    openai_model_client = OpenAIChatCompletionClient(
        model="gpt-5"
    )
    agent1 = AssistantAgent(name="PrimaryAgent", model_client=openai_model_client)
    agent2 = AssistantAgent(name="BackUpAgent", model_client=openai_model_client)

    await Console(agent1.run_stream(
        task="You know what!!!, Superman is my fav superhero"))  # run_stream gives the output in the console line by line. But run will just give you a cumulative result at the end.

    # fetching the state from agent1
    agent1_save_state = await agent1.save_state()

    # open a file in write mode to save the state in json format
    with open(file="state_save_memory.json", mode="w", encoding="utf-8") as f:
        json.dump(agent1_save_state, f, default=str)

    # open the saved json file in read mode to load the state to new agent
    with open(file="state_save_memory.json", mode="r", encoding="utf-8") as f:
        agent2_load_state = json.load(f)

    await agent2.load_state(agent2_load_state)

    await Console(agent2.run_stream(task="whoz my fav superhero?"))

    await openai_model_client.close()


asyncio.run(function_one())
