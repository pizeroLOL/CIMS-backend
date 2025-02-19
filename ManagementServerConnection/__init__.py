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
    def __init__(self, organization_name: str = "ClassIslandManagementServer.py 开发测试"):
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

db.register_client(
    client_uid="26077a30-7859-49c0-aab3-9e04c3ffa270",
    client_id="TEST"
)

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

    async def ListenCommand(self,
                            request_iterator: AsyncIterable[ClientCommandDeliverScReq_pb2.ClientCommandDeliverScReq],
                            context: grpc.aio.ServicerContext) -> AsyncIterable[
        ClientCommandDeliverScRsp_pb2.ClientCommandDeliverScRsp]:
        """
        处理客户端命令监听（双向流）。
        """
        metadata = dict(context.invocation_metadata())
        client_uid = metadata.get('cuid')
        logger.info(f"Client connected: {client_uid}")
        if not client_uid or client_uid not in db.clients:
            logger.warning(f"Client not found or invalid: {client_uid}")
            return

        db.clients[client_uid]["connected"] = True
        response_queue = asyncio.Queue()

        # 异步处理客户端消息
        async def handle_client_messages():
            try:
                async for request in request_iterator:
                    if request.Type == CommandTypes_pb2.Ping:
                        # 处理 Ping 请求
                        logger.debug(f"Received ping from {client_uid}")
                        await response_queue.put(ClientCommandDeliverScRsp_pb2.ClientCommandDeliverScRsp(
                            RetCode=Retcode_pb2.Success,
                            Type=CommandTypes_pb2.Pong
                        ))
                    else:
                        logger.warning(f"Received unknown command type: {request.Type}")
            except Exception as e:
                logger.exception(f"Error handling client messages: {e}")
            finally:
                logger.debug(f"handle_client_messages task finished for {client_uid}")


        # 模拟向客户端发送命令 (例如，每隔一段时间发送 RestartApp)
        async def send_commands():
            try:
                while True:
                    await asyncio.sleep(60)  # 每 60 秒发送一次
                    if client_uid not in db.clients or not db.clients[client_uid]["connected"]:
                        break

                    logger.info(f"Sending RestartApp command to {client_uid}")
                    await response_queue.put(ClientCommandDeliverScRsp_pb2.ClientCommandDeliverScRsp(
                        RetCode=Retcode_pb2.Success,
                        Type=CommandTypes_pb2.RestartApp
                    ))
            except asyncio.CancelledError:
                logger.info(f"send_commands task cancelled for {client_uid}")
            except Exception as e:
                logger.exception(f"Error in send_commands: {e}")
            finally:
                logger.debug(f"send_commands task finished for {client_uid}")

        # Create tasks and add to a set
        tasks = {
            asyncio.create_task(handle_client_messages()),
            asyncio.create_task(send_commands()),
        }

        # Cancellation handling:  This is VERY important.
        def cancel_tasks(fut):
            logger.info(f"gRPC context done, cancelling tasks for {client_uid}")
            for task in tasks:
                task.cancel()
            db.clients.get(client_uid, {})["connected"] = False

        context.add_done_callback(cancel_tasks)


        try:
            while True:
                # Get responses from the queue and yield them
                response = await response_queue.get()
                yield response
        except asyncio.CancelledError:
            logger.info(f"ListenCommand cancelled for {client_uid}")
            for task in tasks:
                task.cancel() # Ensure tasks are cancelled.
            raise
        except Exception as e:
            logger.exception(f"Error in ListenCommand: {e}")
        finally:
            # Clean up
            logger.info(f"ListenCommand finished for {client_uid}")
            db.clients.get(client_uid, {})["connected"] = False


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