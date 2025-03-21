#! -*- coding:utf-8 -*-
from binascii import Incomplete

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
    open(".installed", "w").close()
    installed = False
#endregiono


#region Presets
#region 导入项目内建库
import Datas
import logger
import BuildInClasses
import QuickValues
#endregion


#region 导入辅助库
import argparse
import asyncio
import json
import sys
#endregion


#region 首次运行
if installed:
    pass
else:
    _set = {}

    for part in ["gRPC", "api", "command"]:
        _input = input("gRPC host and port(formatted as http://localhost:50051):")
        _gRPC_set = True
        while _gRPC_set:
            try:
                if _input.startswith("http://"):
                    print("HTTP is not safe and HTTPS recommended.\n" if not _input.startswith("http://localhost") else "",
                          end="")
                _set["gRPC"]["prefix"] = _input.split(":")[0]
                _set["gRPC"]["host"] = _input.split(":")[1][2:]
                _set["gRPC"]["port"] = int(_input.split(":")[2])
                if _set["gRPC"]["port"] not in list(range(1, 65536)):
                    raise KeyError
                _gRPC_set = False
            except IndexError | ValueError:
                _input = input("Invalid input, retry:")
            except KeyError:
                _input = input("Invalid port, retry:")

    _set["organization_name"] = input("Organization name:")

    with open("settings.json", "w") as s:
        json.dump(_set, s)
#endregion
#endregion



