import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ[
    "OPENAI_API_KEY"] = ""


async def function_one():

    openai_model_client = OpenAIChatCompletionClient(
        model="gpt-4o"
    )
    assistant = AssistantAgent(name="MultiModalAssistant", model_client=openai_model_client)

    actual_image = Image.from_file("F:/Projects/mcp_filesystem/pexels-pixabay-163077.jpg")
    multimodal_message = MultiModalMessage(source='user',
                                           content=["What do you see in the image provided?", actual_image])

    await Console(assistant.run_stream(
        task=multimodal_message))  # run_stream gives the output in the console line by line. But run will just give you a cumulative result at the end.
    await openai_model_client.close()


asyncio.run(function_one())
