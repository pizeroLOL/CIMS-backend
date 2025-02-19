# -*- coding: utf-8 -*-
import ManagementServer
import asyncio


async def main():
    await asyncio.gather(
        ManagementServer.gRPC.start(),
        ManagementServer.command.start(),
        ManagementServer.api.start()
    )


if __name__ == "__main__":
    asyncio.run(main())
