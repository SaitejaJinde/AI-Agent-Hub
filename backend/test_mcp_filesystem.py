import asyncio

from tools.mcp_filesystem import (
    list_directory
)


async def main():

    result = await list_directory()

    print(result)


asyncio.run(main())