import json
import os
import time

import uvicorn
from fastapi import FastAPI, HTTPException

api = FastAPI(
    title="Management Server Profiles APIs",
    description="提供客户端配置文件分发服务\n提供客户端配置文件清单",
    version="1.0",
)

DATA_DIR = "Datas"  # 数据存储根目录

# 确保 Datas 目录存在
os.makedirs("Datas", exist_ok=True)

RESOURCE_TYPES = ["Manifests", "Policies", "ClassPlans", "SubjectsSource", "TimeLayouts", "DefaultSettings"]

@api.get("/api/v1/client/{uid}/manifest", summary="获取客户端配置清单")
async def get_client_manifest(id: str=None, uid: str=None, version: int=int(time.time())):
    """获取指定客户端的配置清单"""
    with open(f"Datas/profile_config.json", "r", encoding="utf-8") as f:
        profile_config = json.load(f)
        try:
            return {
                "ClassPlanSource": {
                    "Value": f"http://127.0.0.1:50050/api/client/classPlan?name={profile_config["uid"][uid]["ClassPlan"]}",
                    "Version": version
                },
                "TimeLayoutSource": {
                    "Value": f"http://127.0.0.1:50050/api/client/timeLayout?name={profile_config["uid"][uid]["TimeLayout"]}",
                    "Version": version
                },
                "SubjectsSource": {
                    "Value": f"http://127.0.0.1:50050/api/client/subjects?name={profile_config["uid"][uid]["Subjects"]}",
                    "Version": version
                },
                "DefaultSettingsSource": {
                    "Value": f"http://127.0.0.1:50050/api/client/settings?name={profile_config["uid"][uid]["Settings"]}",
                    "Version": version
                },
                "PolicySource": {
                    "Value": f"http://127.0.0.1:50050/api/client/policy?name={profile_config["uid"][uid]["Policy"]}",
                    "Version": version
                },
                "ServerKind": 1,
                "OrganizationName": "CMS2.py 本地测试"
            }
        except IndexError:
            return {
                "ClassPlanSource": {
                    "Value": f"http://127.0.0.1:50050/api/client/classPlan?name={profile_config["id"][id]["ClassPlan"]}",
                    "Version": version
                },
                "TimeLayoutSource": {
                    "Value": f"http://127.0.0.1:50050/api/client/timeLayout?name={profile_config["id"][id]["TimeLayout"]}",
                    "Version": version
                },
                "SubjectsSource": {
                    "Value": f"http://127.0.0.1:50050/api/client/subjects?name={profile_config["id"][id]["Subjects"]}",
                    "Version": version
                },
                "DefaultSettingsSource": {
                    "Value": f"http://127.0.0.1:50050/api/client/settings?name={profile_config["id"][id]["Settings"]}",
                    "Version": version
                },
                "PolicySource": {
                    "Value": f"http://127.0.0.1:50050/api/client/policy?name={profile_config["id"][id]["Policy"]}",
                    "Version": version
                },
                "ServerKind": 1,
                "OrganizationName": "CMS2.py 本地测试"
            }


@api.get("/api/client/policy", summary="获取策略")
async def get_policy(name: str):
    """获取服务器策略"""
    with open(f"Datas/Policies/{name}.json", "r", encoding="utf-8") as f:
        policy = json.load(f)
    return policy


@api.get("/api/client/classPlan", summary="获取课表")
async def get_class_plan(name: str):
    """获取服务器课表"""
    with open(f"Datas/ClassPlans/{name}.json", "r", encoding="utf-8") as f:
        class_plan = json.load(f)
    return class_plan


@api.get("/api/client/subjects", summary="获取科目列表")
async def get_subjects(name: str):
    """获取科目列表"""
    with open(f"Datas/SubjectsSource/{name}.json", "r", encoding="utf-8") as f:
        subjects = json.load(f)
    return subjects


@api.get("/api/client/timeLayout", summary="获取时间表")
async def get_time_layout(name: str):
    """获取时间表"""
    with open(f"Datas/TimeLayouts/{name}.json", "r", encoding="utf-8") as f:
        time_layout = json.load(f)
    return time_layout


@api.get("/api/client/settings", summary="获取设置")
async def get_settings(name: str):
    """获取设置"""
    with open(f"Datas/DefaultSettings/{name}.json", "r", encoding="utf-8") as f:
        settings = json.load(f)
    return settings


# region 资源管理 API (新增)

@api.get("/api/resources/{resource_type}", summary="获取指定资源类型的文件列表")
async def get_resource_file_list(resource_type: str):
    """
    获取指定资源类型目录下的文件列表。

    - **resource_type**: 资源类型 (Manifests, Policies, ClassPlans, SubjectsSource, TimeLayouts, DefaultSettings)
    """
    if resource_type not in RESOURCE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid resource type")
    resource_dir = os.path.join(DATA_DIR, resource_type)
    if not os.path.exists(resource_dir) or not os.path.isdir(resource_dir):
        return []  # 目录不存在或不是目录，返回空列表
    files = [f for f in os.listdir(resource_dir) if os.path.isfile(os.path.join(resource_dir, f)) and f.endswith(".json")]
    return files


@api.get("/api/resources/{resource_type}/{file_name}", summary="获取指定资源文件的内容")
async def get_resource_file_content(resource_type: str, file_name: str):
    """
    获取指定资源文件的内容。

    - **resource_type**: 资源类型 (Manifests, Policies, ClassPlans, SubjectsSource, TimeLayouts, DefaultSettings)
    - **file_name**: 文件名 (例如：example.json)
    """
    if resource_type not in RESOURCE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid resource type")
    resource_dir = os.path.join(DATA_DIR, resource_type)
    file_path = os.path.join(resource_dir, file_name)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        return content
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")


@api.post("/api/resources/{resource_type}/{file_name}", summary="保存指定资源文件的内容")
async def save_resource_file_content(resource_type: str, file_name: str, content: dict):
    """
    保存指定资源文件的内容。

    - **resource_type**: 资源类型 (Manifests, Policies, ClassPlans, SubjectsSource, TimeLayouts, DefaultSettings)
    - **file_name**: 文件名 (例如：example.json)
    - **content**: 文件内容 (JSON 格式)
    """
    if resource_type not in RESOURCE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid resource type")
    resource_dir = os.path.join(DATA_DIR, resource_type)
    os.makedirs(resource_dir, exist_ok=True)  # 确保目录存在
    file_path = os.path.join(resource_dir, file_name)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4, ensure_ascii=False)
        return {"message": f"File '{file_name}' in '{resource_type}' saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")


# endregion

async def start():
    """<UNK>FastAPI<UNK>"""
    config = uvicorn.Config(app=api, host="127.0.0.1", port=50050, log_level="debug")
    server = uvicorn.Server(config)
    print("Starting API server...")
    await server.serve()

