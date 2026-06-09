import asyncio

from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command="npx",
        args=[
            "@modelcontextprotocol/server-filesystem",
            "."
        ]
    )

    async with stdio_client(server_params) as streams:
        print("Connected to Filesystem MCP Server")


if __name__ == "__main__":
    asyncio.run(main())