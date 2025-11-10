from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools


class McpConfig:

    def __init__(self):
        pass

    async def get_database_tools(self):
        database_server_params = StdioServerParams(
            command="C:\\Users\\<user>\\AppData\\Local\\Programs\\Python\\Python314\\Scripts\\uv.exe",
            args=["--directory",
                  "C:\\Users\\<user>\\AppData\\Local\\Programs\\Python\\Python314\\Lib\\site-packages",
                  "run",
                  "mysql_mcp_server"], env={
                "MYSQL_HOST": "localhost",
                "MYSQL_PORT": "3306",
                "MYSQL_USER": "root",
                "MYSQL_PASSWORD": "",
                "MYSQL_DATABASE": ""
            })
        return await mcp_server_tools(server_params=database_server_params)

    async def get_api_tools(self):
        api_server_params = StdioServerParams(
            command="node",
            args=["C:\\Users\\<user>\\AppData\\Roaming\\npm\\node_modules\\dkmaker-mcp-rest-api\\build\\index.js", ],
            env={
                "REST_BASE_URL": "https://rahulshettyacademy.com",
                "HEADER_Accept": "application/json"
            })
        return await mcp_server_tools(server_params=api_server_params)

    async def get_excel_tools(self):
        excel_server_params = StdioServerParams(
            command="uvx",
            args=["excel-mcp-server", "stdio"]
        )
        return await mcp_server_tools(server_params=excel_server_params)

    async def get_filesystem_tools(self):
        filesystem_server_params = StdioServerParams(
            command="npx",
            args=["-y",
                  "@modelcontextprotocol/server-filesystem",
                  "F:\\Projects\\mcp_filesystem"]
        )
        return await mcp_server_tools(server_params=filesystem_server_params)
