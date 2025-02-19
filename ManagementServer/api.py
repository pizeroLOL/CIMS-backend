import json

import uvicorn
from fastapi import FastAPI, HTTPException

api = FastAPI(
    title="Management Server",
    description="<UNK>",
    version="1.0",
)

@api.get("/api/v1/client/{client_uid}/manifest", summary="获取客户端配置清单")
async def get_client_manifest(client_uid: str):
    """
    获取指定客户端的配置清单

    :param client_uid: 客户端 UUID

    :return 配置清单
    """
    manifest = {
        "ClassPlanSource": {
            "Value": f"http://127.0.0.1:50050/api/v1/client/{client_uid}/classPlan",
            "Version": 1
        },
        "TimeLayoutSource": {
            "Value": f"http://127.0.0.1:50050/api/v1/client/{client_uid}/timeLayout",
            "Version": 1
        },
        "SubjectsSource": {
            "Value": f"http://127.0.0.1:50050/api/v1/client/{client_uid}/subjects",
            "Version": 1
        },
        "DefaultSettingsSource": {
            "Value": f"http://127.0.0.1:50050/api/v1/client/{client_uid}/settings",
            "Version": 1
        },
        "PolicySource": {
            "Value": f"http://127.0.0.1:50050/api/v1/client/{client_uid}/policy",
            "Version": 2
        },
        "ServerKind": 1,
        "OrganizationName": "CMS.py 本地测试"
    }
    return manifest


@api.get("/api/v1/client/{client_uid}/policy", summary="获取策略")
async def get_policy(client_uid: str):
    """获取服务器策略"""
    with open(f"Datas/Policies/{client_uid}.json", "r", encoding="utf-8") as f:
        policy = json.load(f)
    return policy


@api.get("/api/v1/client/{client_uid}/classPlan", summary="获取课表")
async def get_class_plan(client_uid: str):
    """获取服务器课表"""
    with open(f"Datas/ClassPlans/{client_uid}.json", "r", encoding="utf-8") as f:
        class_plan = json.load(f)
    return class_plan


@api.get("/api/v1/client/{client_uid}/subjects", summary="获取科目列表")
async def get_subjects(client_uid: str):
    """获取科目列表"""
    with open(f"Datas/SubjectsSource/{client_uid}.json", "r", encoding="utf-8") as f:
        subjects = json.load(f)
    return subjects


@api.get("/api/v1/client/{client_uid}/timeLayout", summary="获取时间表")
async def get_time_layout(client_uid: str):
    """获取时间表"""
    with open(f"Datas/TimeLayouts/{client_uid}.json", "r", encoding="utf-8") as f:
        time_layout = json.load(f)
    return time_layout


@api.get("/api/v1/client/{client_uid}/settings", summary="获取设置")
async def get_settings(client_uid: str):
    """获取设置"""
    with open(f"Datas/DefaultSettings/{client_uid}.json", "r", encoding="utf-8") as f:
        settings = json.load(f)
    return settings

async def start():
    """<UNK>FastAPI<UNK>"""
    config = uvicorn.Config(app=api, host="127.0.0.1", port=50050, log_level="debug")
    server = uvicorn.Server(config)
    print("Starting API server...")
    await server.serve()

