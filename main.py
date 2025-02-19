# -*- coding: utf-8 -*-
# ClassIslandManagementServer/main.py
import asyncio
import logging
import uuid

import grpc

import launcher as launcher

# 配置日志记录器
from Protobuf.Client import ClientRegisterCsReq_pb2
from Protobuf.Enum import Retcode_pb2
from Protobuf.Service import ClientRegister_pb2_grpc


async def test_client_registration():
    # 启动服务器
    import threading
    threading.Thread(target=launcher.run_server).start()
    # 确保服务器已启动
    await asyncio.sleep(5)
    # 创建与服务器的连接
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        # 创建客户端存根
        stub = ClientRegister_pb2_grpc.ClientRegisterStub(channel)
        # 生成一个随机的客户端 UID
        client_uid = str(uuid.uuid4())

        # 构造注册请求
        request = ClientRegisterCsReq_pb2.ClientRegisterCsReq(
            clientUid=client_uid,
            clientId="TestClient"
        )

        # 调用 Register 方法
        response = await stub.Register(request)

        # 检查响应
        if response.Retcode == Retcode_pb2.Success:
            print("Client registration successful!")
            print(f"Server message: {response.Message}")
        elif response.Retcode == Retcode_pb2.Registered:
            print("Client already registered.")
            print(f"Server message: {response.Message}")
        else:
            print("Client registration failed.")
            print(f"Server message: {response.Message}")
            print(f"Error code: {response.Retcode}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(test_client_registration())
