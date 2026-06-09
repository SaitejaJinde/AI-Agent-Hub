import asyncio

from mcp import ClientSession
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools


async def get_mcp_tools():

    server_params = StdioServerParameters(
        command="npx",
        args=[
            "@modelcontextprotocol/server-filesystem",
            "."
        ]
    )

    async with stdio_client(server_params) as (
        read_stream,
        write_stream
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            tools = await load_mcp_tools(
                session
            )

            return tools


if __name__ == "__main__":

    tools = asyncio.run(
        get_mcp_tools()
    )

    for tool in tools:
        print(tool.name)