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

DATA_DIR = "Datas"
CLIENTS_FILE = os.path.join(DATA_DIR, "clients.json")
CLIENT_STATUS_FILE = os.path.join(DATA_DIR, "client_status.json")
PROFILE_CONFIG_FILE = os.path.join(DATA_DIR, "profile_config.json") # 新增配置文件路径

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

# region 配置文件操作函数 (新增)
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

# region 数据操作函数 (保持不变)
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


class ClientCommandDeliverServicer(ClientCommandDeliver_pb2_grpc.ClientCommandDeliverServicer):
    """客户端命令传递服务 (保持不变)"""
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
    """向指定客户端发送命令 (保持不变)"""
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
    """客户端注册服务 (修改)"""

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

        # 应用默认配置文件
        profile_config = load_profile_config()
        if client_uid not in profile_config:
            profile_config[client_uid] = { # 应用默认配置
                "ClassPlan": "default",
                "Settings": "default",
                "Subjects": "default",
                "Policy": "default",
                "TimeLayout": "default"
            }
            save_profile_config(profile_config)

        return ClientRegisterScRsp_pb2.ClientRegisterScRsp(Retcode=Retcode_pb2.Success,
                                                           Message=f"Client registered: {client_uid}")

    async def UnRegister(self, request, context):
        """客户端注销 (未实现) (保持不变)"""
        # 在实际应用中，你可能需要在这里实现注销逻辑，例如从clients.json中移除客户端
        return ClientRegisterScRsp_pb2.ClientRegisterScRsp(Retcode=Retcode_pb2.ServerInternalError,
                                                           Message="Not implemented")

async def start(port=50051):
    """启动gRPC服务器 (保持不变)"""
    server = grpc.aio.server()
    ClientRegister_pb2_grpc.add_ClientRegisterServicer_to_server(ClientRegisterServicer(), server)
    ClientCommandDeliver_pb2_grpc.add_ClientCommandDeliverServicer_to_server(ClientCommandDeliverServicer(), server)
    listen_addr = f'127.0.0.1:{port}'
    server.add_insecure_port(listen_addr)
    print(f"Starting gRPC server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()