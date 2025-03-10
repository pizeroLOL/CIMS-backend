#! -*- coding:utf-8 -*-
import grpc.aio

#region 导入项目内建库
import Datas
import logger
import BuildInClasses
import QuickValues
#endregion


#region 导入辅助库
import json
import os
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
#endregion


#region 导入 Protobuf 构建文件
from Protobuf.Client import (ClientCommandDeliverScReq_pb2, ClientCommandDeliverScReq_pb2_grpc,
                             ClientRegisterCsReq_pb2, ClientRegisterCsReq_pb2_grpc)
from Protobuf.Command import (SendNotification_pb2, SendNotification_pb2_grpc,
                              HeartBeat_pb2, HeartBeat_pb2_grpc)
from Protobuf.Enum import (CommandTypes_pb2, CommandTypes_pb2_grpc,
                           Retcode_pb2, Retcode_pb2_grpc)
from Protobuf.Server import (ClientCommandDeliverScRsp_pb2, ClientCommandDeliverScRsp_pb2_grpc,
                             ClientRegisterScRsp_pb2, ClientRegisterScRsp_pb2_grpc)
from Protobuf.Service import (ClientCommandDeliver_pb2, ClientCommandDeliver_pb2_grpc,
                              ClientRegister_pb2, ClientRegister_pb2_grpc)
#endregion


#region 导入配置文件
class _Settings:
    def __init__(self):
        self.conf_name:str = "settings.json"
        self.conf_dict:dict = json.load(open(self.conf_name))

    @property
    async def refresh(self) -> dict:
        self.conf_dict = json.load(open(self.conf_name))
        return self.conf_dict

Settings = _Settings()
#endregion


#region 内建辅助函数和辅助参量
log = logger.Logger()
#endregion


#region 命令传递通道服务
class ClientCommandDeliverServicer(ClientCommandDeliver_pb2_grpc.ClientCommandDeliverServicer):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ClientCommandDeliverServicer, cls).__new__(cls, *args, **kwargs)
            cls._instance.clients = {}  # 用于存储客户端流 {client_uid: context}
            cls._instance.executor = ThreadPoolExecutor(max_workers=10)
        return cls._instance

    async def ListenCommand(self, request_iterator, context:grpc.aio.ServicerContext):
        metadata = context.invocation_metadata()
        client_uid = metadata["cuid"]
        log.log("Client {client_uid} connected.".format(client_uid=client_uid), QuickValues.Log.info)
        self.clients[client_uid] = context
        Datas.ClientStatus.update(client_uid)

#endregion

