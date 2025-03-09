#! -*- coding:utf-8 -*-


#region 导入项目内建库
import Datas
import logger
import BuildInClasses
import QuickValues
#endregion


#region 导入辅助库
import time
import json
#endregion


#region 导入 FastAPI 相关库
import uvicorn
from fastapi import FastAPI
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
api = FastAPI()
#endregion


#region 内建辅助函数和辅助参量
async def _get_manifest_entry(base_url, name, version, host, port):
    return {
        "Value": "{host}:{port}{base_url}?name={name}".format(
            base_url=base_url, name=name, host=host, port=port),
        "Version": version, }


log = logger.Logger()
#endregion


#region 配置文件分发 APIs
@api.get("/api/v1/client/{client_uid}/manifest")
async def manifest(uid:str | None=None, version:int=int(time.time())) -> dict:
    organization_name = Settings.conf_dict.get("OrganizationName", "CMS2.py 本地测试")
    host = "http://" + Settings.conf_dict.get("host", "127.0.0.1")
    port = Settings.conf_dict.get("port", 50050)

    """获取指定客户端的配置清单"""
    profile_config = Datas.ProfileConfig.profile_config
    base_url = "/api/v1/client/"
    config = profile_config.get(uid, {"ClassPlan": "default", "TimeLayout": "default", "Subjects": "default",
                                      "Settings": "default", "Policy": "default"})
    return {
        "ClassPlanSource": await _get_manifest_entry(f"{base_url}ClassPlan", config["ClassPlan"], version, host, port),
        "TimeLayoutSource": await _get_manifest_entry(f"{base_url}TimeLayout", config["TimeLayout"], version, host, port),
        "SubjectsSource": await _get_manifest_entry(f"{base_url}Subjects", config["Subjects"], version, host, port),
        "DefaultSettingsSource": await _get_manifest_entry(f"{base_url}DefaultSettings", config["Settings"], version, host, port),
        "PolicySource": await _get_manifest_entry(f"{base_url}Policy", config["Policy"], version, host, port),
        "ServerKind": 1,
        "OrganizationName": Settings.conf_dict.get("OrganizationName", "CIMS default organization"),
    }


@api.get("/api/v1/client/{resource_type}")
async def policy(resource_type, name:str) -> dict:
    match resource_type:
        case "ClassPlan" | "DefaultSettings" | "Policy" | "Subjects" | "TimeLayout":
            return getattr(Datas, resource_type).read(name)
        case _:
            raise HTTPException(status_code=404)
#endregion


#region 外部操作方法
@api.get("/api/refresh")
async def refresh() -> None:
    _ = Settings.refresh
    return None
#endregion


#region 启动函数
async def start(port:int=50050):
    config = uvicorn.Config(app=api, port=port, host="0.0.0.0", log_level="debug")
    server = uvicorn.Server(config)
    await server.serve()
    print("API server successfully start on {port}".format(port=port))
#endregion


#region 不接受直接运行
if __name__ == "__main__":
    log.log(message="Directly started, refused.", status=QuickValues.Log.error)
#endregion
