import asyncio

from mcp import ClientSession
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

    async with stdio_client(server_params) as (
        read_stream,
        write_stream
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            tools = await session.list_tools()

            print(tools)


if __name__ == "__main__":
    asyncio.run(main())