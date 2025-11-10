from autogen_agentchat.agents import AssistantAgent

from Framework.MCP_Config import McpConfig


class AgentFactory:

    def __init__(self, model_client):
        self.model_client = model_client
        self.mcp_config = McpConfig()

    async def create_database_agent(self, system_message):
        db_tools = await self.mcp_config.get_database_tools()
        database_agent = AssistantAgent(name="DatabaseAgent", model_client=self.model_client,
                                        tools=db_tools,
                                        system_message=system_message)
        return database_agent

    async def create_api_agent(self, system_message):
        api_tools = await self.mcp_config.get_api_tools()
        api_agent = AssistantAgent(name="APIAgent", model_client=self.model_client,
                                   tools=api_tools,
                                   system_message=system_message)
        return api_agent

    async def create_excel_agent(self, system_message):
        excel_tools = await self.mcp_config.get_excel_tools()
        fs_tools = await self.mcp_config.get_filesystem_tools()
        excel_agent = AssistantAgent(name="ExcelAgent", model_client=self.model_client,
                                     tools=[excel_tools, fs_tools],
                                     system_message=system_message)
        return excel_agent
