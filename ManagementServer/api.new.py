import Datas, time, json, argparse

import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, PlainTextResponse, RedirectResponse, StreamingResponse
from fastapi.exceptions import HTTPException


class _Settings:
    def __init__(self):
        self.conf_name:str = "settings.json"
        self.conf_dict:dict = json.load(open(self.conf_name))

    @property
    async def refresh(self) -> dict:
        self.conf_dict = json.load(open(self.conf_name))
        return self.conf_dict

Settings = _Settings()


api = FastAPI()

_get_manifest_entry = lambda base_url, name, version, host, port: {
    "Value": "{host}:{port}{base_url}?name={name}".format(
        base_url=base_url, name=name, host=host, port=port),
    "Version": version, }

@api.get("/api/v1/client/{client_uid}/manifest")
async def manifest(uid:str | None=None, version:int=int(time.time())):
    organization_name = Settings.conf_dict.get("OrganizationName", "CMS2.py 本地测试")
    host = "http://" + Settings.conf_dict.get("host", "127.0.0.1")
    port = Settings.conf_dict.get("port", 50050)

    """获取指定客户端的配置清单"""
    profile_config = Datas.ProfileConfig.profile_config
    base_url = "/api/v1/client/"
    config = profile_config.get(uid, {"ClassPlan": "default", "TimeLayout": "default", "Subjects": "default",
                                      "Settings": "default", "Policy": "default"})
    return {
        "ClassPlanSource": _get_manifest_entry(f"{base_url}ClassPlans", config["ClassPlan"], version, host, port),
        "TimeLayoutSource": _get_manifest_entry(f"{base_url}TimeLayouts", config["TimeLayout"], version, host, port),
        "SubjectsSource": _get_manifest_entry(f"{base_url}SubjectsSource", config["Subjects"], version, host, port),
        "DefaultSettingsSource": _get_manifest_entry(f"{base_url}Settings", config["Settings"], version, host, port),
        "PolicySource": _get_manifest_entry(f"{base_url}Policies", config["Policy"], version, host, port),
        "ServerKind": 1,
        "OrganizationName": Settings.conf_dict.get("OrganizationName", "CIMS default organization"),
    }
