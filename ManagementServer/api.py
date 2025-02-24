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
PROFILE_CONFIG_FILE = os.path.join(DATA_DIR, "profile_config.json") # 配置文件路径

# 确保 Datas 目录存在
os.makedirs("Datas", exist_ok=True)

# 使用字典映射 profile_type 到目录名
PROFILE_TYPE_DIRECTORIES = {
    "ClassPlan": "ClassPlans",
    "Settings": "DefaultSettings",
    "Policy": "Policies",
    "Subjects": "SubjectsSource",
    "TimeLayout": "TimeLayouts"
}

PROFILE_TYPES = list(PROFILE_TYPE_DIRECTORIES.keys()) # 从字典中动态生成 PROFILE_TYPES
RESOURCE_TYPES = list(PROFILE_TYPE_DIRECTORIES.values()) # 从字典中动态生成 RESOURCE_TYPES (用于资源管理 API)


# region 配置文件操作函数 (保持不变)
def load_profile_config():
    """加载配置文件"""
    if os.path.exists(PROFILE_CONFIG_FILE):
        with open(PROFILE_CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_profile_config(profile_config):
    """保存配置文件"""
    with open(PROFILE_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(profile_config, f, indent=4, ensure_ascii=False)

# endregion

# region 客户端配置相关 API (修改)
@api.get("/api/v1/client/{uid}/manifest", summary="获取客户端配置清单")
async def get_client_manifest(id: str=None, uid: str=None, version: int=int(time.time())):
    """获取指定客户端的配置清单"""
    profile_config = load_profile_config()
    client_profile = profile_config.get(uid, {}) # 获取客户端特定的配置，如果不存在则为空字典
    return {
        "ClassPlanSource": {
            "Value": f"http://127.0.0.1:50050/api/client/classPlan?name={client_profile.get('ClassPlan', 'default')}", # 使用 client_profile 中的配置，默认为 default
            "Version": version
        },
        "TimeLayoutSource": {
            "Value": f"http://127.0.0.1:50050/api/client/timeLayout?name={client_profile.get('TimeLayout', 'default')}", # 使用 client_profile 中的配置，默认为 default
            "Version": version
        },
        "SubjectsSource": {
            "Value": f"http://127.0.0.1:50050/api/client/subjects?name={client_profile.get('Subjects', 'default')}", # 使用 client_profile 中的配置，默认为 default
            "Version": version
        },
        "DefaultSettingsSource": {
            "Value": f"http://127.0.0.1:50050/api/client/settings?name={client_profile.get('Settings', 'default')}", # 使用 client_profile 中的配置，默认为 default
            "Version": version
        },
        "PolicySource": {
            "Value": f"http://127.0.0.1:50050/api/client/policy?name={client_profile.get('Policy', 'default')}", # 使用 client_profile 中的配置，默认为 default
            "Version": version
        },
        "ServerKind": 1,
        "OrganizationName": "CMS2.py 本地测试"
    }


@api.get("/api/client/policy", summary="获取策略")
async def get_policy(name: str):
    """获取服务器策略"""
    policy_dir = os.path.join(DATA_DIR, PROFILE_TYPE_DIRECTORIES["Policy"]) # 使用字典获取目录名
    policy_file_path = os.path.join(policy_dir, f"{name}.json")
    if not os.path.exists(policy_file_path):
        raise HTTPException(status_code=404, detail="Policy file not found")
    with open(policy_file_path, "r", encoding="utf-8") as f:
        policy = json.load(f)
    return policy


@api.get("/api/client/classPlan", summary="获取课表")
async def get_class_plan(name: str):
    """获取课表"""
    class_plan_dir = os.path.join(DATA_DIR, PROFILE_TYPE_DIRECTORIES["ClassPlan"]) # 使用字典获取目录名
    class_plan_file_path = os.path.join(class_plan_dir, f"{name}.json")
    if not os.path.exists(class_plan_file_path):
        raise HTTPException(status_code=404, detail="ClassPlan file not found")
    with open(class_plan_file_path, "r", encoding="utf-8") as f:
        class_plan = json.load(f)
    return class_plan


@api.get("/api/client/subjects", summary="获取科目列表")
async def get_subjects(name: str):
    """获取科目列表"""
    subjects_dir = os.path.join(DATA_DIR, PROFILE_TYPE_DIRECTORIES["Subjects"]) # 使用字典获取目录名
    subjects_file_path = os.path.join(subjects_dir, f"{name}.json")
    if not os.path.exists(subjects_file_path):
        raise HTTPException(status_code=404, detail="Subjects file not found")
    with open(subjects_file_path, "r", encoding="utf-8") as f:
        subjects = json.load(f)
    return subjects


@api.get("/api/client/timeLayout", summary="获取时间表")
async def get_time_layout(name: str):
    """获取时间表"""
    time_layout_dir = os.path.join(DATA_DIR, PROFILE_TYPE_DIRECTORIES["TimeLayout"]) # 使用字典获取目录名
    time_layout_file_path = os.path.join(time_layout_dir, f"{name}.json")
    if not os.path.exists(time_layout_file_path):
        raise HTTPException(status_code=404, detail="TimeLayout file not found")
    with open(time_layout_file_path, "r", encoding="utf-8") as f:
        time_layout = json.load(f)
    return time_layout


@api.get("/api/client/settings", summary="获取设置")
async def get_settings(name: str):
    """获取设置"""
    settings_dir = os.path.join(DATA_DIR, PROFILE_TYPE_DIRECTORIES["Settings"]) # 使用字典获取目录名
    settings_file_path = os.path.join(settings_dir, f"{name}.json")
    if not os.path.exists(settings_file_path):
        raise HTTPException(status_code=404, detail="Settings file not found")
    with open(settings_file_path, "r", encoding="utf-8") as f:
        settings = json.load(f)
    return settings

# endregion

# region 资源管理 API (保持不变，但 RESOURCE_TYPES 已更新)

@api.get("/api/resources/{resource_type}", summary="获取指定资源类型的文件列表")
async def get_resource_file_list(resource_type: str):
    """
    获取指定资源类型目录下的文件列表。

    - **resource_type**: 资源类型 (ClassPlans, DefaultSettings, Policies, SubjectsSource, TimeLayouts)
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