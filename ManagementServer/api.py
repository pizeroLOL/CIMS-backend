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
    if uid in [i for i in Datas.ProfileConfig.refresh()]:
        profile_config = Datas.ProfileConfig.profile_config
        _return =  {
            "ClassPlanSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/classPlan?name={profile_config[uid]['ClassPlan']}", # 使用 client_profile 中的配置，默认为 default
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
    """
    拉取策略
    :param name: 策略名称
    :return: 拉取的策略
    """
    try:
        return Datas.Policies.read_file(name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Policy file not found.")


@api.get("/api/v1/client/classPlan", summary="获取课表")
async def get_class_plan(name: str):
    """获取课表"""
    try:
        return Datas.ClassPlans.read_file(name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Class plan file not found.")


@api.get("/api/v1/client/subjects", summary="获取科目列表")
async def get_subjects(name: str):
    """获取科目列表"""
    try:
        return Datas.SubjectsSource.read_file(name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Subject source file not found.")

@api.get("/api/v1/client/timeLayout", summary="获取时间表")
async def get_time_layout(name: str):
    """获取时间表"""
    try:
        return Datas.TimeLayouts.read_file(name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Time layout file not found.")


@api.get("/api/v1/client/settings", summary="获取设置")
async def get_settings(name: str):
    """获取设置"""
    try:
        return Datas.DefaultSettings.read_file(name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Settings file not found.")

# endregion

# region 资源管理 API (保持不变，但 RESOURCE_TYPES 已更新)

@api.get("/api/v1/panel/{resource_type}", summary="获取指定资源类型的文件列表")
async def get_resource_file_list(resource_type: str):
    """
    获取指定资源类型目录下的文件列表。

    - **resource_type**: 资源类型 (ClassPlans, DefaultSettings, Policies, SubjectsSource, TimeLayouts)
    """
    match resource_type:
        case "ClassPlans":
            return Datas.ClassPlans.refresh()
        case "DefaultSettings":
            return Datas.DefaultSettings.refresh()
        case "Policies":
            return Datas.Policies.refresh()
        case "SubjectsSource":
            return Datas.SubjectsSource.refresh()
        case "TimeLayouts":
            return Datas.TimeLayouts.refresh()
        case _:
            raise HTTPException(status_code=404, detail="Resource type invalid.")


@api.post("/api/resources/{resource_type}/{file_name}", summary="保存指定资源文件的内容")
async def save_resource_file_content(resource_type: str, file_name: str, content: dict):
    """
    保存指定资源文件的内容。

    - **resource_type**: 资源类型 (ClassPlans, DefaultSettings, Policies, SubjectsSource, TimeLayouts)
    - **file_name**: 文件名 (例如：default.json)
    - **content**: 文件内容 (JSON 格式)
    """
    try:
        match resource_type:
            case "ClassPlans":
                return Datas.ClassPlans.write_file(file_name, content)
            case "DefaultSettings":
                return Datas.DefaultSettings.write_file(file_name, content)
            case "Policies":
                return Datas.Policies.write_file(file_name, content)
            case "SubjectsSource":
                return Datas.SubjectsSource.write_file(file_name, content)
            case "TimeLayouts":
                return Datas.TimeLayouts.write_file(file_name, content)
            case _:
                raise HTTPException(status_code=404, detail="Resource type invalid.")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=e)

# endregion




async def start(port=50050):
    """<UNK>FastAPI<UNK>"""
    config = uvicorn.Config(app=api, port=port, log_level="debug")
    server = uvicorn.Server(config)
    print("Starting API server...")
    await server.serve()