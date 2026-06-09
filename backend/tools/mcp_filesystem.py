from mcp import ClientSession
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client


async def list_directory(path="."):

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

            result = await session.call_tool(
                "list_directory",
                {
                    "path": path
                }
            )

            return result.structuredContent["content"]


async def read_mcp_file(file_path):

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

            result = await session.call_tool(
                "read_file",
                {
                    "path": file_path
                }
            )

            return result.structuredContent["content"]