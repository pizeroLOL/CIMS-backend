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
                "Value": f"http://127.0.0.1:50050/api/v1/client/ClassPlan?name={profile_config[uid]['ClassPlan']}", # 使用 client_profile 中的配置，默认为 default
                "Version": version
            },
            "TimeLayoutSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/TimeLayout?name={profile_config[uid]['TimeLayout']}", # 使用 client_profile 中的配置，默认为 default
                "Version": version
            },
            "SubjectsSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/Subjects?name={profile_config[uid]['Subjects']}", # 使用 client_profile 中的配置，默认为 default
                "Version": version
            },
            "DefaultSettingsSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/Settings?name={profile_config[uid]['Settings']}", # 使用 client_profile 中的配置，默认为 default
                "Version": version
            },
            "PolicySource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/Policy?name={profile_config[uid]['Policy']}", # 使用 client_profile 中的配置，默认为 default
                "Version": version
            },
            "ServerKind": 1,
            "OrganizationName": "CMS2.py 本地测试"
        }
        return _return
    else:
        return {
            "ClassPlanSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/ClassPlan?name=default",
                "Version": version
            },
            "TimeLayoutSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/TimeLayout?name=default",
                "Version": version
            },
            "SubjectsSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/Subjects?name=default",
                "Version": version
            },
            "DefaultSettingsSource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/Settings?name=default",
                "Version": version
            },
            "PolicySource": {
                "Value": f"http://127.0.0.1:50050/api/v1/client/Policy?name=default",
                "Version": version
            },
            "ServerKind": 1,
            "OrganizationName": "CMS2.py 本地测试"
        }


@api.get("/api/v1/client/Policies", summary="获取策略")
async def get_policies(name: str):
    """
    拉取策略
    :param name: 策略名称
    :return: 拉取的策略
    """
    try:
        return Datas.Policies.read(name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Policy file not found.")


@api.get("/api/v1/client/ClassPlans", summary="获取课表")
async def get_class_plans(name: str):
    """获取课表"""
    try:
        return Datas.ClassPlans.read(name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Class plan file not found.")


@api.get("/api/v1/client/SubjectsSource", summary="获取科目列表")
async def get_subjects_source(name: str):
    """获取科目列表"""
    try:
        return Datas.SubjectsSource.read(name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Subject source file not found.")

@api.get("/api/v1/client/TimeLayouts", summary="获取时间表")
async def get_time_layouts(name: str):
    """获取时间表"""
    try:
        return Datas.TimeLayouts.read(name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Time layout file not found.")


@api.get("/api/v1/client/DefaultSettings", summary="获取设置")
async def get_default_settings(name: str):
    """获取设置"""
    try:
        return Datas.DefaultSettings.read(name)
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


@api.get("/api/v1/panel/new/{resource_type}", summary="新文件")
async def new_resource(resource_type: str):
    match resource_type:
        case "ClassPlans":
            return Datas.ClassPlans.new(name=resource_type)
        case "DefaultSettings":
            return Datas.DefaultSettings.new(name=resource_type)
        case "Policies":
            return Datas.Policies.new(name=resource_type)
        case "SubjectsSource":
            return Datas.SubjectsSource.new(name=resource_type)
        case "TimeLayouts":
            return Datas.TimeLayouts.new(name=resource_type)
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
                return Datas.ClassPlans.write(file_name, content)
            case "DefaultSettings":
                return Datas.DefaultSettings.write(file_name, content)
            case "Policies":
                return Datas.Policies.write(file_name, content)
            case "SubjectsSource":
                return Datas.SubjectsSource.write(file_name, content)
            case "TimeLayouts":
                return Datas.TimeLayouts.write(file_name, content)
            case _:
                raise HTTPException(status_code=404, detail="Resource type invalid.")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=e)

# endregion




async def start(port=50050, host="0.0.0.0"):
    """<UNK>FastAPI<UNK>"""
    config = uvicorn.Config(app=api, port=port, host=host, log_level="debug")
    server = uvicorn.Server(config)
    print("Starting API server...")
    await server.serve()