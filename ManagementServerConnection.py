import asyncio
import json
import os
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

import grpc
import uvicorn
from fastapi import FastAPI, HTTPException, Depends

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
    if os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


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


# endregion

# region gRPC服务

class ClientCommandDeliverServicer(ClientCommandDeliver_pb2_grpc.ClientCommandDeliverServicer):
    """客户端命令传递服务"""
    _instance = None  # 单例实例

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ClientCommandDeliverServicer, cls).__new__(cls, *args, **kwargs)
            cls._instance.clients = {}  # 用于存储客户端流 {client_uid: context}
            cls._instance.executor = ThreadPoolExecutor(max_workers=10)
        return cls._instance

    async def ListenCommand(self, request_iterator, context: grpc.aio.ServicerContext):
        """监听客户端命令"""
        md = context.invocation_metadata()
        client_uid = ""
        for m in md:
            if m.key == 'cuid':
                client_uid = m.value
        if not client_uid:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Client UID is required.")
            return
        print(f"Client connected: {client_uid}")
        self.clients[client_uid] = context  # 使用 self.clients
        client_status = load_client_status()
        client_status[client_uid] = {
            "isOnline": True,
            "lastHeartbeat": time.time()
        }
        save_client_status(client_status)

        try:
            async for request in request_iterator:
                if request.Type == CommandTypes_pb2.Ping:
                    # 处理心跳
                    client_status = load_client_status()
                    client_status[client_uid] = {
                        "isOnline": True,
                        "lastHeartbeat": time.time()
                    }
                    save_client_status(client_status)
                    # print(f"Received ping from {client_uid}")
                    await context.write(ClientCommandDeliverScRsp_pb2.ClientCommandDeliverScRsp(
                        RetCode=Retcode_pb2.Success,
                        Type=CommandTypes_pb2.Pong
                    ))
        except Exception as e:
            print(f"Client disconnected: {client_uid} - {e}")
        finally:
            self.clients.pop(client_uid, None)  # 使用 self.clients
            client_status = load_client_status()
            if client_uid in client_status:
                client_status[client_uid] = {
                    "isOnline": False,
                    "lastHeartbeat": time.time()
                }
                save_client_status(client_status)


async def send_command(client_uid: str, command_type: CommandTypes_pb2.CommandTypes, payload: bytes = b''):
    """向指定客户端发送命令"""
    servicer = ClientCommandDeliverServicer()  # 获取单例实例
    if client_uid not in servicer.clients:
        raise HTTPException(status_code=404, detail=f"Client not found or not connected: {client_uid}")
    context = servicer.clients[client_uid]
    await context.write(ClientCommandDeliverScRsp_pb2.ClientCommandDeliverScRsp(
        RetCode=Retcode_pb2.Success,
        Type=command_type,
        Payload=payload
    ))


class ClientRegisterServicer(ClientRegister_pb2_grpc.ClientRegisterServicer):
    """客户端注册服务"""

    async def Register(self, request: ClientRegisterCsReq_pb2.ClientRegisterCsReq,
                       context: grpc.aio.ServicerContext) -> ClientRegisterScRsp_pb2.ClientRegisterScRsp:
        """客户端注册"""
        clients = load_clients()
        client_uid = request.clientUid
        client_id = request.clientId
        if client_uid in clients:
            # 更新客户端名称
            clients.update({
                client_uid: client_id
            })
            save_clients(clients)
            return ClientRegisterScRsp_pb2.ClientRegisterScRsp(Retcode=Retcode_pb2.Registered,
                                                               Message=f"Client already registered: {client_uid}")
        clients[client_uid] = client_id
        save_clients(clients)
        client_status = load_client_status()
        client_status[client_uid] = {
            "isOnline": True,
            "lastHeartbeat": time.time()
        }
        save_client_status(client_status)
        return ClientRegisterScRsp_pb2.ClientRegisterScRsp(Retcode=Retcode_pb2.Success,
                                                           Message=f"Client registered: {client_uid}")

    async def UnRegister(self, request, context):
        """客户端注销 (未实现)"""
        # 在实际应用中，你可能需要在这里实现注销逻辑，例如从clients.json中移除客户端
        return ClientRegisterScRsp_pb2.ClientRegisterScRsp(Retcode=Retcode_pb2.ServerInternalError,
                                                           Message="Not implemented")


# endregion

# region FastAPI接口
command = FastAPI(title="ClassIsland Management Server",
                  description="集控服务器API",
                  version="1.0.0", )


@command.get("/clients", summary="获取所有已注册客户端")
async def get_clients():
    """获取所有已注册的客户端列表"""
    return load_clients()


@command.get("/clients/status", summary="获取所有客户端状态")
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
            clients = load_clients()
            del clients[k]
            save_clients(clients)

    return status


@command.get("/clients/{client_uid}/status", summary="获取指定客户端状态")
async def get_client_status(client_uid: str):
    """
    获取指定客户端的状态。

    - **client_uid**: 客户端的唯一标识符。
    """
    status = load_client_status()
    if client_uid not in status:
        raise HTTPException(status_code=404, detail="Client status not found")
    return status[client_uid]


@command.post("/clients/{client_uid}/restart", summary="重启指定客户端")
async def restart_client(client_uid: str):
    """
    对指定客户端执行重新启动操作。

    - **client_uid**: 客户端的唯一标识符。
    """
    await send_command(client_uid, CommandTypes_pb2.RestartApp)
    return {"message": f"Restart command sent to client: {client_uid}"}


@command.post("/clients/{client_uid}/notify", summary="向指定客户端发送消息")
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


@command.post("/clients/{client_uid}/update", summary="更新指定客户端数据")
async def update_client_data(client_uid: str):
    """
    对指定客户端执行更新数据操作。

    - **client_uid**: 客户端的唯一标识符。
    """
    await send_command(client_uid, CommandTypes_pb2.DataUpdated)
    return {"message": f"Data update command sent to client: {client_uid}"}


api = FastAPI(
    title="Management Server",
    description="<UNK>",
    version="1.0",
)

@api.get("/api/v1/client/{client_uid}/manifest", summary="获取客户端配置清单")
async def get_client_manifest(client_uid: str):
    """
    获取指定客户端的配置清单（模拟）。

    - **client_uid**: 客户端的唯一标识符。
    """
    # 这里应该根据实际情况返回客户端的配置清单，这里只是一个示例
    manifest = {
        "ServerKind": 1,
        "OrganizationName": "示例组织",
        "PolicySource": {
            "value": f"/api/v1/policy",
            "version": 1
        }
        # 其他配置...
    }
    return manifest


@api.get("/api/v1/policy", summary="获取策略")
async def get_policy():
    """获取服务器策略（模拟）。"""
    # 这里应该根据实际情况返回策略，这里只是一个示例
    policy = {
        "allowExitManagement": True,
        # 其他策略...
    }
    return policy


# endregion

# region 启动服务器

async def start_grpc_server():
    """启动gRPC服务器"""
    server = grpc.aio.server()
    ClientRegister_pb2_grpc.add_ClientRegisterServicer_to_server(ClientRegisterServicer(), server)
    ClientCommandDeliver_pb2_grpc.add_ClientCommandDeliverServicer_to_server(ClientCommandDeliverServicer(), server)
    listen_addr = f'127.0.0.1:50051'
    server.add_insecure_port(listen_addr)
    print(f"Starting gRPC server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()


async def start_command_server():
    """启动FastAPI服务器"""
    config = uvicorn.Config(app=command, host="127.0.0.1", port=50052, log_level="debug")
    server = uvicorn.Server(config)
    print("Starting Command server...")
    await server.serve()


async def start_api_server():
    """<UNK>FastAPI<UNK>"""
    config = uvicorn.Config(app=api, host="127.0.0.1", port=50050, log_level="debug")
    server = uvicorn.Server(config)
    print("Starting API server...")
    await server.serve()


async def main():
    await asyncio.gather(
        start_grpc_server(),
        start_command_server(),
        start_api_server()
    )


if __name__ == "__main__":
    asyncio.run(main())
# endregion