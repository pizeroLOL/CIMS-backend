# -*- coding: utf-8 -*-
# file: ClassIslandManagementServer/client/ManagementServerConnection/__init__.py
import asyncio
import json
import logging
import uuid
from asyncio import Future
from typing import Dict, Optional, AsyncIterable
import grpc

from Protobuf.Client import ClientCommandDeliverScReq_pb2, ClientRegisterCsReq_pb2
from Protobuf.Enum import CommandTypes_pb2, Retcode_pb2
from Protobuf.Server import ClientCommandDeliverScRsp_pb2, ClientRegisterScRsp_pb2
from Protobuf.Service import ClientCommandDeliver_pb2_grpc, ClientRegister_pb2_grpc

# 配置日志记录器
logger = logging.getLogger(__name__)


# 定义 ManagementManifest 类（根据 C# 代码推断）
class ManagementManifest:
    def __init__(self, organization_name: str = "Default Organization"):
        self.OrganizationName = organization_name


# 模拟数据库或配置存储
class Database:
    clients: Dict[str, Dict] = {}
    manifest: ManagementManifest = ManagementManifest()
    def get_manifest(self) -> ManagementManifest:
        return self.manifest
    def register_client(self, client_uid: str, client_id: str) -> Retcode_pb2.Retcode:
        """
        注册客户端。

        Args:
            client_uid: 客户端唯一ID。
            client_id: 客户端ID（例如班级标识）。

        Returns:
            注册结果代码。
        """
        if client_uid in self.clients:
            return Retcode_pb2.Registered  # 客户端已注册
        self.clients[client_uid] = {
            "id": client_id,
            "connected": False  # 新注册的客户端默认未连接
        }
        return Retcode_pb2.Success
# 模拟数据库实例
db = Database()

# 实现 ClientRegister 服务
class ClientRegisterServicer(ClientRegister_pb2_grpc.ClientRegisterServicer):
    async def Register(self, request: ClientRegisterCsReq_pb2.ClientRegisterCsReq,
                       context: grpc.aio.ServicerContext) -> ClientRegisterScRsp_pb2.ClientRegisterScRsp:
        """
        处理客户端注册请求。
        """
        logger.info(f"Received registration request: clientUid={request.clientUid}, clientId={request.clientId}")
        retcode = db.register_client(request.clientUid, request.clientId)
        message = "Client registered successfully." if retcode == Retcode_pb2.Success else "Client already registered."
        return ClientRegisterScRsp_pb2.ClientRegisterScRsp(Retcode=retcode, Message=message)

    async def UnRegister(self, request, context):
        # TODO: 实现客户端注销逻辑
        pass


# 实现 ClientCommandDeliver 服务
class ClientCommandDeliverServicer(ClientCommandDeliver_pb2_grpc.ClientCommandDeliverServicer):

    async def ListenCommand(self, request_iterator: AsyncIterable[ClientCommandDeliverScReq_pb2.ClientCommandDeliverScReq]
                             , context: grpc.aio.ServicerContext) -> AsyncIterable[ClientCommandDeliverScRsp_pb2.ClientCommandDeliverScRsp]:
        """
        处理客户端命令监听（双向流）。
        """
        metadata = dict(context.invocation_metadata())
        client_uid = metadata.get('cuid')
        logger.info(f"Client connected: {client_uid}")
        db.clients.get(client_uid, {})["connected"] = True

        # 异步处理客户端消息
        async def handle_client_messages():
            async for request in request_iterator:
                if request.Type == CommandTypes_pb2.Ping:
                    # 处理 Ping 请求
                    logger.debug(f"Received ping from {client_uid}")
                    yield ClientCommandDeliverScRsp_pb2.ClientCommandDeliverScRsp(
                        RetCode=Retcode_pb2.Success,
                        Type=CommandTypes_pb2.Pong
                    )
                else:
                    logger.warning(f"Received unknown command type: {request.Type}")

        # 模拟向客户端发送命令 (例如，每隔一段时间发送 RestartApp)
        async def send_commands():
            while True:
                await asyncio.sleep(60)  # 每 60 秒发送一次
                if client_uid not in db.clients or not db.clients[client_uid]["connected"]:
                    break

                logger.info(f"Sending RestartApp command to {client_uid}")
                yield ClientCommandDeliverScRsp_pb2.ClientCommandDeliverScRsp(
                    RetCode=Retcode_pb2.Success,
                    Type=CommandTypes_pb2.RestartApp
                )
        try:
            async for response in asyncio.as_completed([handle_client_messages(), send_commands()]):
                yield await response
        except asyncio.CancelledError as e:
            logger.info(f"Client {client_uid} disconnected.")
            if client_uid and client_uid in db.clients:
                db.clients[client_uid]["connected"] = False
            raise e

# HTTP 服务 (使用 aiohttp)
from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/api/v1/client/{client_uid}/manifest')
async def get_manifest(request: web.Request):
    """
    处理获取管理清单的 HTTP 请求。
    """
    client_uid = request.match_info['client_uid']
    logger.info(f"Received manifest request for client: {client_uid}")
    # TODO: 根据 client_uid 确定返回的清单内容（如果需要）
    manifest = db.get_manifest()
    return web.json_response({
        "OrganizationName": manifest.OrganizationName
        # 添加其他清单字段...
    })

async def create_app():
    app = web.Application()
    app.add_routes(routes)

    # 启动 gRPC 服务器
    server = grpc.aio.server()
    ClientRegister_pb2_grpc.add_ClientRegisterServicer_to_server(ClientRegisterServicer(), server)
    ClientCommandDeliver_pb2_grpc.add_ClientCommandDeliverServicer_to_server(ClientCommandDeliverServicer(), server)
    listen_addr = '[::]:50051'  # 监听地址
    server.add_insecure_port(listen_addr)
    logger.info(f"Starting server on {listen_addr}")
    await server.start()

    async def server_graceful_shutdown():
        logger.info("Shutting down gRPC server...")
        await server.stop(5)
        logger.info("gRPC server shut down.")

    app.on_shutdown.append(lambda _: server_graceful_shutdown)

    return app

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(create_app())
