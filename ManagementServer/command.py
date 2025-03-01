import asyncio
import json
import os
import time
import Datas

import uvicorn
from fastapi import FastAPI, HTTPException

from ManagementServer.gRPC import send_command

# 导入生成的protobuf和grpc文件
from Protobuf.Client import ClientCommandDeliverScReq_pb2, ClientRegisterCsReq_pb2
from Protobuf.Command import SendNotification_pb2
from Protobuf.Enum import CommandTypes_pb2, Retcode_pb2
from Protobuf.Server import ClientCommandDeliverScRsp_pb2, ClientRegisterScRsp_pb2
from Protobuf.Service import (ClientCommandDeliver_pb2_grpc,
                              ClientRegister_pb2_grpc)

# 数据存储目录
DATA_DIR = "Datas"
CLIENTS_FILE = os.path.join(DATA_DIR, "clients.json")
CLIENT_STATUS_FILE = os.path.join(DATA_DIR, "client_status.json")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)


# region 数据操作函数
def load_clients():
    """加载客户端列表"""
    return Datas.Clients.refresh()


def save_clients(clients):
    """保存客户端列表"""
    with open(CLIENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(clients, f, indent=4, ensure_ascii=False)


def load_client_status():
    """加载客户端状态"""
    if os.path.exists(CLIENT_STATUS_FILE):
        with open(CLIENT_STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_client_status(status):
    """保存客户端状态"""
    with open(CLIENT_STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=4, ensure_ascii=False)

command = FastAPI(title="ClassIsland Management Server",
                  description="集控服务器API",
                  version="1.0.0", )


@command.get("/command/clients", summary="获取所有已注册客户端")
async def get_clients():
    """获取所有已注册的客户端列表"""
    return load_clients()


@command.get("/command/clients/status", summary="获取所有客户端状态")
async def get_all_client_status():
    """
    获取所有客户端的状态。
    """
    status = load_client_status()
    # 清理长时间离线客户端
    t = time.time()
    for k in list(status.keys()):
        if t - status[k]["lastHeartbeat"] > 60 * 5:  # 5分钟
            print(f"清理离线客户端：{k}")
            del status[k]
            save_client_status(status)
            # clients = load_clients()
            # del clients[k]
            # save_clients(clients)

    return status


@command.get("/command/clients/{client_uid}/status", summary="获取指定客户端状态")
async def get_client_status(client_uid: str):
    """
    获取指定客户端的状态。

    - **client_uid**: 客户端的唯一标识符。
    """
    status = load_client_status()
    if client_uid not in status:
        raise HTTPException(status_code=404, detail="Client status not found")
    return status[client_uid]


@command.post("/command/clients/{client_uid}/restart", summary="重启指定客户端")
async def restart_client(client_uid: str):
    """
    对指定客户端执行重新启动操作。

    - **client_uid**: 客户端的唯一标识符。
    """
    await send_command(client_uid, CommandTypes_pb2.RestartApp)
    return {"message": f"Restart command sent to client: {client_uid}"}


@command.post("/command/clients/{client_uid}/notify", summary="向指定客户端发送消息")
async def send_notification(client_uid: str,
                            message_mask: str,
                            message_content: str,
                            overlay_icon_left: int = 0,
                            overlay_icon_right: int = 0,
                            is_emergency: bool = False,
                            is_speech_enabled: bool = True,
                            is_effect_enabled: bool = True,
                            is_sound_enabled: bool = True,
                            is_topmost: bool = True,
                            duration_seconds: float = 5.0,
                            repeat_counts: int = 1):
    """
    对指定客户端执行发送消息操作。

    - **client_uid**: 客户端的唯一标识符。
    - **message_mask**: 消息遮罩文本
    - **message_content**: 消息内容
    - **overlay_icon_left**: 左侧图标
    - **overlay_icon_right**: 右侧图标
    - **is_emergency**: 是否紧急消息
    - **is_speech_enabled**: 是否启用语音
    - **is_effect_enabled**: 是否启用特效
    - **is_sound_enabled**: 是否启用声音
    - **is_topmost**: 是否置顶
    - **duration_seconds**: 持续时间（秒）
    - **repeat_counts**: 重复次数
    """
    notification = SendNotification_pb2.SendNotification(
        MessageMask=message_mask,
        MessageContent=message_content,
        OverlayIconLeft=overlay_icon_left,
        OverlayIconRight=overlay_icon_right,
        IsEmergency=is_emergency,
        IsSpeechEnabled=is_speech_enabled,
        IsEffectEnabled=is_effect_enabled,
        IsSoundEnabled=is_sound_enabled,
        IsTopmost=is_topmost,
        DurationSeconds=duration_seconds,
        RepeatCounts=repeat_counts
    )
    payload = notification.SerializeToString()
    await send_command(client_uid, CommandTypes_pb2.SendNotification, payload)
    return {"message": f"Notification sent to client: {client_uid}"}


@command.post("/command/clients/{client_uid}/update", summary="更新指定客户端数据")
async def update_client_data(client_uid: str):
    """
    对指定客户端执行更新数据操作。

    - **client_uid**: 客户端的唯一标识符。
    """
    await send_command(client_uid, CommandTypes_pb2.DataUpdated)
    return {"message": f"Data update command sent to client: {client_uid}"}


async def start(port=50052):
    """启动FastAPI服务器"""
    config = uvicorn.Config(app=command, port=port, host="0.0.0.0", log_level="debug")
    server = uvicorn.Server(config)
    print("Starting Command server...")
    await server.serve()

