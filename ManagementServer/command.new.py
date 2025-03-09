#! -*- coding:utf-8 -*-


#region 导入项目内建库
import Datas
import logger
import BuildInClasses
import QuickValues
#endregion


#region 导入辅助库
import json
#endregion


#region 导入 FastAPI 相关库
import uvicorn
from fastapi import FastAPI, Query
from fastapi.requests import Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, PlainTextResponse, RedirectResponse, StreamingResponse
from fastapi.exceptions import HTTPException
#endregion


#region 导入配置文件
class _Settings:
    def __init__(self):
        self.conf_name:str = "settings.json"
        self.conf_dict:dict = json.load(open(self.conf_name))

    @property
    async def refresh(self) -> dict:
        self.conf_dict = json.load(open(self.conf_name))
        return self.conf_dict

Settings = _Settings()
#endregion


#region 定义 API
command = FastAPI()
#endregion


#region 内建辅助函数和辅助参量
log = logger.Logger()
#endregion


#region 配置文件管理相关 API
@command.get("/command/datas/{resource_type}/create")
async def create(resource_type:str, name:str) -> None:
    match resource_type:
        case "ClassPlan" | "DefaultSettings" | "Policy" | "Subjects" | "TimeLayout":
            return getattr(Datas, resource_type).new(name)
        case _:
            raise HTTPException(status_code=404)


@command.delete("/command/datas/{resource_type}")
@command.delete("/command/datas/{resource_type}/")
@command.delete("/command/datas/{resource_type}/delete")
@command.get("/command/datas/{resource_type}/delete")
async def delete(resource_type:str, name:str) -> None:
    match resource_type:
        case "ClassPlan" | "DefaultSettings" | "Policy" | "Subjects" | "TimeLayout":
            return getattr(Datas, resource_type).delete(name)
        case _:
            raise HTTPException(status_code=404)


@command.get("/command/datas/{resource_type}/list")
async def _list(resource_type:str) -> list[str]:
    match resource_type:
        case "ClassPlan" | "DefaultSettings" | "Policy" | "Subjects" | "TimeLayout":
            return getattr(Datas, resource_type).refresh()
        case _:
            raise HTTPException(status_code=404)


@command.get("/command/datas/{resource_type}/rename")
async def rename(resource_type:str, name:str, target:str) -> None:
    match resource_type:
        case "ClassPlan" | "DefaultSettings" | "Policy" | "Subjects" | "TimeLayout":
            return getattr(Datas, resource_type).rename(name, target)
        case _:
            raise HTTPException(status_code=404)


@command.put("/command/datas/{resource_type}")
@command.put("/command/datas/{resource_type}/")
@command.put("/command/datas/{resource_type}/write")
@command.post("/command/datas/{resource_type}")
@command.post("/command/datas/{resource_type}/")
@command.post("/command/datas/{resource_type}/write")
@command.get("/command/datas/{resource_type}/write")
async def write(resource_type:str, name:str, request:Request):
    match resource_type:
        case "ClassPlan" | "DefaultSettings" | "Policy" | "Subjects" | "TimeLayout":
            return getattr(Datas, resource_type).write(name, await request.body())
        case _:
            raise HTTPException(status_code=404)
#endregion


#region 客户端管理相关 API
# TODO:客户端管理相关 API
#endregion


#region 外部操作方法
@command.get("/command/refresh")
async def refresh() -> None:
    _ = Settings.refresh
    return None
#endregion


#region 启动函数
async def start(port:int=50052):
    config = uvicorn.Config(app=command, port=port,log_level="debug")
    server = uvicorn.Server(config)
    await server.serve()
    print("Command backend successfully start on {port}".format(port=port))
#endregion


#region 不接受直接运行
if __name__ == "__main__":
    log.log(message="Directly started, refused.", status=QuickValues.Log.error)
#endregion
