from aiohttp.web_response import Response

import Datas
import time

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

api = FastAPI(
    title="Management Server Profiles APIs",
    description="提供客户端配置文件分发服务\n提供客户端配置文件清单",
    version="1.0",
)


@api.get("/favicon.ico")
async def favicon():
    return FileResponse("./webui/public/favicon.ico")


# region 客户端配置相关 API (修改)
@api.get("/api/v1/client/{uid}/manifest", summary="获取客户端配置清单")
async def get_client_manifest(uid: str=None, version: int=int(time.time())):
    """获取指定客户端的配置清单"""
    if uid in [i for i in Datas.get.ProfileConfig.refresh()]:
        profile_config = Datas.get.ProfileConfig.profile_config
        _return =  {
            "ClassPlanSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/classPlan?name={profile_config[uid]["ClassPlan"]}", # 使用 client_profile 中的配置，默认为 default
                "Version": version
            },
            "TimeLayoutSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/timeLayout?name={profile_config[uid]['TimeLayout']}", # 使用 client_profile 中的配置，默认为 default
                "Version": version
            },
            "SubjectsSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/subjects?name={profile_config[uid]['Subjects']}", # 使用 client_profile 中的配置，默认为 default
                "Version": version
            },
            "DefaultSettingsSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/settings?name={profile_config[uid]['Settings']}", # 使用 client_profile 中的配置，默认为 default
                "Version": version
            },
            "PolicySource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/policy?name={profile_config[uid]['Policy']}", # 使用 client_profile 中的配置，默认为 default
                "Version": version
            },
            "ServerKind": 1,
            "OrganizationName": "CMS2.py 本地测试"
        }
        return _return
    else:
        return {
            "ClassPlanSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/classPlan?name=default",
                "Version": version
            },
            "TimeLayoutSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/timeLayout?name=default",
                "Version": version
            },
            "SubjectsSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/subjects?name=default",
                "Version": version
            },
            "DefaultSettingsSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/settings?name=default",
                "Version": version
            },
            "PolicySource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/policy?name=default",
                "Version": version
            },
            "ServerKind": 1,
            "OrganizationName": "CMS2.py 本地测试"
        }


@api.get("/api/v1/client/policy", summary="获取策略")
async def get_policy(name: str):
    """获取服务器策略"""
    try:
        return Datas.get.Policies.read_file(name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Policy file not found.")


@api.get("/api/client/classPlan", summary="获取课表")
async def get_class_plan(name: str):
    """获取课表"""
    try:
        return Datas.get.ClassPlans.read_file(name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Class plan file not found.")


@api.get("/api/client/subjects", summary="获取科目列表")
async def get_subjects(name: str):
    """获取科目列表"""
    try:
        return Datas.get.SubjectsSource[name]
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Subject source file not found.")

@api.get("/api/client/timeLayout", summary="获取时间表")
async def get_time_layout(name: str):
    """获取时间表"""
    try:
        return Datas.get.TimeLayouts[name]
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Time layout file not found.")


@api.get("/api/client/settings", summary="获取设置")
async def get_settings(name: str):
    """获取设置"""
    try:
        return Datas.get.DefaultSettings[name]
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Settings file not found.")

# endregion

# region 资源管理 API (保持不变，但 RESOURCE_TYPES 已更新)

@api.get("/api/resources/{resource_type}", summary="获取指定资源类型的文件列表")
async def get_resource_file_list(resource_type: str):
    """
    获取指定资源类型目录下的文件列表。

    - **resource_type**: 资源类型 (ClassPlans, DefaultSettings, Policies, SubjectsSource, TimeLayouts)
    """
    match resource_type:
        case "ClassPlans":
            return Datas.get.ClassPlans.refresh()
        case "DefaultSettings":
            return Datas.get.DefaultSettings.refresh()
        case "Policies":
            return Datas.get.Policies.refresh()
        case "SubjectsSource":
            return Datas.get.SubjectsSource.refresh()
        case "TimeLayouts":
            return Datas.get.TimeLayouts.refresh()
        case _:
            raise HTTPException(status_code=404, detail="Resource type invalid.")


@api.get("/api/resources/{resource_type}/{file_name}", summary="获取指定资源文件的内容")
async def get_resource_file_content(resource_type: str, file_name: str):
    """
    获取指定资源文件的内容。

    - **resource_type**: 资源类型 (ClassPlans, DefaultSettings, Policies, SubjectsSource, TimeLayouts)
    - **file_name**: 文件名 (例如：default.json)
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

    - **resource_type**: 资源类型 (ClassPlans, DefaultSettings, Policies, SubjectsSource, TimeLayouts)
    - **file_name**: 文件名 (例如：default.json)
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

# region 客户端 Profile 配置 API (保持不变)

@api.get("/api/v1/client/{client_uid}/profileConfig", summary="获取指定客户端的 Profile 配置")
async def get_client_profile_config(client_uid: str):
    """
    获取指定客户端的 Profile 配置。
    """
    profile_config = load_profile_config()
    client_profile = profile_config.get(client_uid, {})
    return client_profile

@api.post("/api/v1/client/{client_uid}/profileConfig", summary="保存指定客户端的 Profile 配置")
async def save_client_profile_config(client_uid: str, profile_config_data: dict):
    """
    保存指定客户端的 Profile 配置。
    """
    profile_config = load_profile_config()
    profile_config[client_uid] = profile_config_data
    save_profile_config(profile_config)
    return {"message": f"Profile config for client '{client_uid}' saved successfully"}

@api.get("/api/v1/profiles/names/{profile_type}", summary="获取指定 Profile 类型的文件名列表")
async def get_profile_names(profile_type: str):
    """
    获取指定 Profile 类型的文件名列表。
    """
    if profile_type not in PROFILE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid profile type")
    profile_dir = os.path.join(DATA_DIR, PROFILE_TYPE_DIRECTORIES[profile_type]) # 使用字典获取目录名
    if not os.path.exists(profile_dir) or not os.path.isdir(profile_dir):
        return []
    files = [f.replace(".json", "") for f in os.listdir(profile_dir) if os.path.isfile(os.path.join(profile_dir, f)) and f.endswith(".json")]
    return files


# endregion


async def start():
    """<UNK>FastAPI<UNK>"""
    config = uvicorn.Config(app=api, host="127.0.0.1", port=50050, log_level="debug")
    server = uvicorn.Server(config)
    print("Starting API server...")
    await server.serve()