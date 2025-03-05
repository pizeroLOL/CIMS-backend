import Datas
import time
import json
import argparse

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

def _get_manifest_entry(base_url, name, version, host, port=50050):
    return {
        "Value": f"http://{host}:{port}{base_url}?name={name}",
        "Version": version
    }

def _load_settings(settings_file="settings.json"):
    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}



@api.get("/api/v1/client/{uid}/manifest", summary="获取客户端配置清单")
async def get_client_manifest(uid: str=None, version: int=int(time.time()), settings_file: str = "settings.json"):
    settings = _load_settings(settings_file)
    organization_name = settings.get("OrganizationName", "CMS2.py 本地测试")
    host = settings.get("Host", "127.0.0.1:50050")

    """获取指定客户端的配置清单"""
    profile_config = Datas.ProfileConfig.profile_config
    base_url = "/api/v1/client/"
    config = profile_config.get(uid, {"ClassPlan": "default", "TimeLayout": "default", "Subjects": "default", "Settings": "default", "Policy": "default"})
    return {
        "ClassPlanSource": _get_manifest_entry(f"{base_url}ClassPlan", config["ClassPlan"], version, host),
        "TimeLayoutSource": _get_manifest_entry(f"{base_url}TimeLayout", config["TimeLayout"], version, host),
        "SubjectsSource": _get_manifest_entry(f"{base_url}Subjects", config["Subjects"], version, host),
        "DefaultSettingsSource": _get_manifest_entry(f"{base_url}Settings", config["Settings"], version, host),
        "PolicySource": _get_manifest_entry(f"{base_url}Policy", config["Policy"], version, host),
        "ServerKind": 1,
        "OrganizationName": organization_name
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
async def new_resource(resource_type: str, name: str):
    """Create a new resource file of the specified type."""
    match resource_type:
        case "ClassPlans" | "DefaultSettings" | "Policies" | "SubjectsSource" | "TimeLayouts":
            resource_manager = getattr(Datas, resource_type)
            return resource_manager.new(name=name)
        case _:
            raise HTTPException(status_code=404, detail="Resource type invalid.")


@api.delete("/api/v1/panel/{resource_type}/{file_name}", summary="删除指定资源文件")
async def delete_resource_file(resource_type: str, file_name: str):
    """
    删除指定资源文件。

    - **resource_type**: 资源类型 (ClassPlans, DefaultSettings, Policies, SubjectsSource, TimeLayouts)
    - **file_name**: 文件名 (例如：default.json)
    """
    match resource_type:
        case "ClassPlans" | "DefaultSettings" | "Policies" | "SubjectsSource" | "TimeLayouts":
            resource_manager = getattr(Datas, resource_type)
            return resource_manager.delete(file_name)
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
    """启动 FastAPI 应用"""
    parser = argparse.ArgumentParser(description="启动管理服务器")
    parser.add_argument("--port", type=int, default=port, help="服务器端口号")
    parser.add_argument("--host", type=str, default=host, help="服务器主机地址")
    parser.add_argument("--settings", type=str, default="settings.json", help="配置文件路径")

    args = parser.parse_args()

    settings = _load_settings(args.settings)
    port = settings.get("Port", args.port)
    host = settings.get("Host", args.host)

    config = uvicorn.Config(app=api, port=port, host=host, log_level="debug", reload=True)
    server = uvicorn.Server(config)
    print("Starting API server...")
    await server.serve()


if __name__ == "__main__":
    import asyncio

    asyncio.run(start())

