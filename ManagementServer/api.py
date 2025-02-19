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
    # 这里应该根据实际情况返回客户端的配置清单，这里只是一个示例
    manifest = {
        "ServerKind": 1,
        "OrganizationName": "示例组织",
        "PolicySource": {
            "value": f"http://127.0.0.1:50050/api/v1/client/{client_uid}/policy",
            "version": 2
        }
        # 其他配置...
    }
    return manifest


@api.get("/api/v1/client/{client_uid}/policy", summary="获取策略")
async def get_policy(client_uid: str):
    """获取服务器策略（模拟）。"""
    # 这里应该根据实际情况返回策略，这里只是一个示例
    policy = {
    "DisableProfileClassPlanEditing": True,
    "DisableProfileTimeLayoutEditing": True,
    "DisableProfileSubjectsEditing": True,
    "DisableProfileEditing": True,
    "DisableSettingsEditing": True,
    "DisableSplashCustomize": True,
    "DisableDebugMenu": True,
    "AllowExitManagement": False
}
    return policy

async def start():
    """<UNK>FastAPI<UNK>"""
    config = uvicorn.Config(app=api, host="127.0.0.1", port=50050, log_level="debug")
    server = uvicorn.Server(config)
    print("Starting API server...")
    await server.serve()

