#! -*- coding:utf-8 -*-

#region Only directly run allowed.
if __name__ !=  "__main__":
    import sys
    sys.exit(0)
#endregion


#region 首次运行判定
try:
    open(".installed").close()
    installed = True
except FileNotFoundError:
    installed = False
#endregiono


#region 导入辅助库
import argparse
import asyncio
import json
from json import JSONDecodeError
import sys
#endregion


#region 检查 settings.json
try:
    with open("settings.json") as f:
        json.load(f)
except JSONDecodeError:
    with open("settings.json", "w") as f:
        f.write("{}")
        f.close()
except FileNotFoundError:
        f.write("{}")
        f.close()
#endregion


#region Presets
#region 导入项目内建库
import Datas
import logger
import BuildInClasses
import QuickValues
import ManagementServer
#endregion


#region 首次运行
if installed:
    with open("settings.json") as s:
        _set = json.load(s)
else:
    _set = {
        "gRPC": {
            "prefix": "http",
            "host": "localhost",
            "port": 50051
        },
        "api": {
            "prefix": "http",
            "host": "localhost",
            "port": 50051
        },
        "command": {
            "prefix": "http",
            "host": "localhost",
            "port": 50051
        },
        "organization_name": "CIMS Default Organization",
    }

    for part in ["gRPC", "api", "command"]:
        _input = input("{part} host and port(formatted as http://localhost:80 and port must be given):".format(part=part))
        _part_set = True
        while _part_set:
            try:
                if _input.startswith("http://"):
                    print("HTTP is not safe and HTTPS recommended.\n" if not _input.startswith("http://localhost") else "",
                          end="")
                if not _input.startswith(("https://", "http://")):
                    raise ValueError
                _set[part]["prefix"] = _input.split(":")[0] + "://"
                _set[part]["host"] = _input.split(":")[1][2:]
                _set[part]["port"] = int(_input.split(":")[2])
                # if _set[part]["port"] not in list(range(-1, 65536)):
                #     raise KeyError
                _part_set = False
            except IndexError | ValueError:
                _input = input("Invalid input, retry:")
            except KeyError:
                _input = input("Invalid port, retry:")

    _set["organization_name"] = input("Organization name:")

    with open("settings.json", "w") as s:
        json.dump(_set, s)

    open(".installed", "w").close()
#endregion


#region 传参初始化
parser = argparse.ArgumentParser(
    description="ClassIsland Management Server Backend"
)

parser.add_argument(
    "-g",
    "--generate-management-preset",
    action="store_true",
    help="Generate ManagementPreset.json on the program root."
)

parser.add_argument(
    "-r",
    "--restore",
    action="store_true",
    help="Restore, and delete all existed data"
)

args = parser.parse_args()
#endregion
#endregion


#region 启动器
async def start():
    await asyncio.gather(
        ManagementServer.gRPC.start(_set["gRPC"]["port"]),
        ManagementServer.api.start(_set["api"]["port"]),
        ManagementServer.command.start(_set["command"]["port"]),
    )
#endregion


#region 操作函数
if args.restore:
    if input("Continue?(y/n with default n)") in ("y", "Y"):
        import os
        os.remove(".installed")
        os.remove("settings.json")
        os.remove("ManagementPreset.json")
        if input("Remove datas?"):
            # for _json in ["./Datas/client_status.json", "./Datas/clients.json", "./"]
            pass
elif args.generate_management_preset:
    with open("ManagementPreset.json", "w") as mp:
        json.dump({
            "ManagementServerKind": 1,
            "ManagementServer": "{prefix}{host}:{port}".format(prefix=_set["api"]["prefix"],
                                                               host=_set["api"]["host"],
                                                               port=_set["api"]["port"]),
            "ManagementServerGrpc": "{prefix}{host}:{port}".format(prefix=_set["gRPC"]["prefix"],
                                                                   host=_set["gRPC"]["host"],
                                                                   port=_set["gRPC"]["port"])
        }, mp)
else:
    asyncio.run(start())
#endregion
