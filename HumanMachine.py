import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ[
    "OPENAI_API_KEY"] = ""


async def function_one():

    openai_model_client = OpenAIChatCompletionClient(
        model="gpt-4o"
    )
    assistant = AssistantAgent(name="MachineAgentMathsTutor", model_client=openai_model_client, system_message="You are helpful math tutor.Help the user solve math problems step by step." 
    "When user acknowledges with THANKS, reply with SESSION COMPLETE.")

    user_proxy = UserProxyAgent(name="Student")

    prompts = RoundRobinGroupChat(participants=[user_proxy, assistant], termination_condition=TextMentionTermination("SESSION COMPLETE"))

    await Console(prompts.run_stream(
        task="I need help to understand Trigonometry. Please help me understand easily"))  # run_stream gives the output in the console line by line. But run will just give you a cumulative result at the end.
    await openai_model_client.close()


asyncio.run(function_one())
