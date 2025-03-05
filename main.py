# -*- coding: utf-8 -*-
import ManagementServer
import asyncio
import json

try:
    with open("settings.json") as s:
        settings = json.load(s)
except FileNotFoundError:
    settings = {
        "ports": {
            "gRPC": 50051,
            "command": 50052,
            "api": 50050,
            "webui": 50053,
        },
        "organization_name": "CMS2.py 本地测试",
        "host": "0.0.0.0"
    }
    with open("settings.json", "w") as s:
        json.dump(settings, s, indent=4)




async def main():
    await asyncio.gather(
        ManagementServer.gRPC.start(settings["ports"]["gRPC"]),
        ManagementServer.command.start(settings["ports"]["command"]),
        ManagementServer.api.start(settings["ports"]["api"])
    )


if __name__ == "__main__":
    asyncio.run(main())
