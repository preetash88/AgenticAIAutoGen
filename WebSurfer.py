import asyncio
import os

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.models.openai import OpenAIChatCompletionClient


os.environ[
    "OPENAI_API_KEY"] = ""

#Fetch the list of model your API_KEY has access to
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# response = client.models.list()  # or similar depending on sdk
# for model in response.data:
#     print(model.id)


#first install using <pip install "autogen-ext[web-surfer]" in the terminal>

async def function_one():
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o")
    web_surfer_agent = MultimodalWebSurfer(name="WebSurfer", model_client=model_client, headless=False,
                                           animate_actions=True)
    agent_team = RoundRobinGroupChat(participants=[web_surfer_agent], max_turns=3)

    await Console(agent_team.run_stream(
        task="Navigate to Google and search for 'AutoGen framework Python'. Then summarize what "
             "you find."))  # run_stream gives the output in the console line by line. But run will just give you a cumulative result at the end.

    await web_surfer_agent.close()
    await model_client.close()


asyncio.run(function_one())
