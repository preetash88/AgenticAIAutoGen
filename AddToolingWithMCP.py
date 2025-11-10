import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools

os.environ[
    "OPENAI_API_KEY"] = ""


# file system mcp
# {
#   "mcpServers": {
#     "filesystem": {
#       "command": "npx",
#       "args": [
#         "-y",
#         "@modelcontextprotocol/server-filesystem",
#         "/Users/username/Desktop",
#         "/path/to/other/allowed/dir"
#       ]
#     }
#   }
# }

async def function_one():
    # Setup server params for local filesystem access
    server_params = StdioServerParams(command="npx", args=["-y",
                                                           "@modelcontextprotocol/server-filesystem",
                                                           "F:\\Projects\\mcp_filesystem"], read_timeout_seconds=60)

    # Get all available tools from the server
    tools = await mcp_server_tools(server_params)

    # Create an agent that can use all the tools
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o"
    )
    assistant = AssistantAgent(name="MachineAgentMathsTutor", model_client=model_client, tools=tools,
                               system_message="You are helpful math tutor.Help the user solve math problems step by step.You also have access to file system"
                                              "When user acknowledges with THANKS, reply with SESSION COMPLETE.")

    user_proxy = UserProxyAgent(name="Student")

    prompts = RoundRobinGroupChat(participants=[user_proxy, assistant],
                                  termination_condition=TextMentionTermination("SESSION COMPLETE"))

    await Console(prompts.run_stream(
        task="I need help to understand Trigonometry. Please help me understand easily. Tutor, feel free to create files to help with student learning"))  # run_stream gives the output in the console line by line. But run will just give you a cumulative result at the end.
    await model_client.close()


asyncio.run(function_one())
