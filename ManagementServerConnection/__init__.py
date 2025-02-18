import json
import os
import time
import grpc
import asyncio # 引入 asyncio

# 导入生成的 gRPC 代码
from proto_python_out.Protobuf.Service import ClientCommandDeliver_pb2 as ClientCommandDeliver_pb2
from proto_python_out.Protobuf.Service import ClientCommandDeliver_pb2_grpc as ClientCommandDeliver_pb2_grpc
from proto_python_out.Protobuf.Service import ClientRegister_pb2 as ClientRegister_pb2
from proto_python_out.Protobuf.Service import ClientRegister_pb2_grpc as ClientRegister_pb2_grpc
from proto_python_out.Protobuf.Client import ClientCommandDeliverScReq_pb2 as ClientCommandDeliverScReq_pb2
from proto_python_out.Protobuf.Client import ClientRegisterCsReq_pb2 as ClientRegisterCsReq_pb2
from proto_python_out.Protobuf.Server import ClientCommandDeliverScRsp_pb2 as ClientCommandDeliverScRsp_pb2
from proto_python_out.Protobuf.Server import ClientRegisterScRsp_pb2 as ClientRegisterScRsp_pb2
from proto_python_out.Protobuf.Enum import CommandTypes_pb2 as CommandTypes_pb2
from proto_python_out.Protobuf.Enum import Retcode_pb2 as Retcode_pb2
from proto_python_out.Protobuf.Command import HeartBeat_pb2 as HeartBeat_pb2
from proto_python_out.Protobuf.Command import SendNotification_pb2 as SendNotification_pb2


class ManagementServerKind:
    Serverless = "Serverless"
    ManagementServer = "ManagementServer"

class AuthorizeLevel:
    NoneLevel = "None"
    User = "User"
    Admin = "Admin"

class CommandTypes: # 使用生成的 Enum
    DefaultCommand = CommandTypes_pb2.DefaultCommand
    ServerConnected = CommandTypes_pb2.ServerConnected
    Ping = CommandTypes_pb2.Ping
    Pong = CommandTypes_pb2.Pong
    RestartApp = CommandTypes_pb2.RestartApp
    SendNotification = CommandTypes_pb2.SendNotification
    DataUpdated = CommandTypes_pb2.DataUpdated

class Retcode: # 使用生成的 Enum
    NoneCode = Retcode_pb2.NoneCode
    Success = Retcode_pb2.Success
    ServerInternalError = Retcode_pb2.ServerInternalError
    InvalidRequest = Retcode_pb2.InvalidRequest
    Registered = Retcode_pb2.Registered
    ClientNotFound = Retcode_pb2.ClientNotFound


class ClientCommandEventArgs: # 模拟 C# ClientCommandEventArgs
    def __init__(self, type, payload=None):
        self.type = type
        self.payload = payload

class ManagementVersions: # 模拟 C# ManagementVersions
    def __init__(self):
        self.policy_version = None

class ManagementManifest: # 模拟 C# ManagementManifest
    def __init__(self):
        self.organization_name = None
        self.policy_source = None # 可以是一个 URL 字符串

class ManagementSettings: # 模拟 C# ManagementSettings
    def __init__(self):
        self.is_management_enabled = False
        self.management_server_kind = ManagementServerKind.Serverless
        self.management_server = None # 服务器地址
        self.management_server_grpc = None # gRPC 服务器地址
        self.manifest_url_template = None
        self.class_identity = None

class ManagementPolicy: # 模拟 C# ManagementPolicy
    def __init__(self):
        self.allow_exit_management = True # 示例策略

class ManagementCredentialConfig: # 模拟 C# ManagementCredentialConfig
    def __init__(self):
        self.admin_credential = None
        self.user_credential = None
        self.exit_management_authorize_level = AuthorizeLevel.Admin

class ManagementClientPersistConfig: # 模拟 C# ManagementClientPersistConfig
    def __init__(self):
        self.client_unique_id = None #  应为唯一标识符，例如 UUID

class ManagementServerConnectionInterface: # 定义连接接口，方便后续扩展和替换
    def get_manifest(self):
        raise NotImplementedError

    def save_json_async(self, url, path):
        raise NotImplementedError

    def register_async(self):
        raise NotImplementedError

    def listen_commands(self):
        raise NotImplementedError

    def close_connection(self):
        raise NotImplementedError


class ManagementServerConnection(ManagementServerConnectionInterface): # 模拟 C# ManagementServerConnection
    """
    用于与集控服务器建立连接并进行通信的类。
    处理 gRPC 连接、命令监听、心跳等。
    """
    def __init__(self, settings, client_uid, light_connect=False):
        """
        初始化 ManagementServerConnection 实例。

        Args:
            settings (ManagementSettings): 集控设置对象。
            client_uid (str): 客户端唯一 ID。
            light_connect (bool): 是否轻量连接，如果为 True，则不立即监听命令。
        """
        self.logger = self._get_logger() #  需要您实现一个 logger 获取方法
        self.client_guid = client_uid
        self.id = settings.class_identity or ""
        self.host = settings.management_server
        self.management_settings = settings
        self.manifest_url = f"{self.host}/api/v1/client/{client_uid}/manifest"
        self.command_connection_alive_timer_interval = 10 # 秒
        self.command_listening_call = None #  模拟 gRPC 流
        self.command_listening_call_cancellation_token_source = False #  模拟 CancellationTokenSource
        self.command_received_event = None #  模拟 C# 的事件，可以使用回调函数列表

        self.channel = self._create_grpc_channel(settings.management_server_grpc) #  创建 gRPC Channel
        self.logger.info("初始化管理服务器连接。")
        if not light_connect:
            self.listen_commands()

    def _get_logger(self):
        """
        获取 logger 实例的占位符方法。
        您需要根据您的日志框架实现此方法。
        """
        #  TODO: 实现获取 logger 的逻辑
        print("Logger placeholder: 请配置您的日志系统")
        class DummyLogger: #  一个简单的占位 logger
            def info(self, msg): print(f"INFO: {msg}")
            def warning(self, msg): print(f"WARNING: {msg}")
            def error(self, msg, exc_info=None, stack_info=False): print(f"ERROR: {msg}, Exception: {exc_info}") # 添加 stack_info 参数
            def debug(self, msg): print(f"DEBUG: {msg}")

        return DummyLogger()


    def _create_grpc_channel(self, grpc_server_address):
        """
        创建 gRPC 通道。
        使用 grpc 库连接到指定的 gRPC 服务器地址。
        """
        try:
            print(f"gRPC Channel: 连接到 {grpc_server_address}")
            channel = grpc.aio.insecure_channel(grpc_server_address) # 使用 grpc.aio.insecure_channel 创建异步 insecure channel
            return channel # 返回 gRPC Channel 实例
        except Exception as e:
            self.logger.error(f"创建 gRPC Channel 失败: {e}", exc_info=True)
            return None


    async def register_async(self):
        """
        向集控服务器注册客户端实例。
        使用 gRPC ClientRegister 服务进行注册。
        """
        self.logger.info("正在注册实例")
        client = ClientRegister_pb2_grpc.ClientRegisterStub(self.channel) # 获取注册客户端 Stub
        try:
            request = ClientRegisterCsReq_pb2.ClientRegisterCsReq(clientUid=self.client_guid, clientId=self.id) # 创建注册请求
            response = await client.Register(request) # 执行注册请求 (异步调用)
            self.logger.debug(f"ClientRegisterClient.RegisterAsync: {response.retcode} {response.message}")
            if response.retcode != Retcode.Registered and response.retcode != Retcode.Success:
                raise Exception(f"无法注册实例：{response.message}")
            return await self.get_manifest()
        except grpc.RpcError as e: # 捕获 gRPC 异常
            self.logger.error(f"注册实例失败: {e.details()}", exc_info=True) # 打印详细错误信息
            raise

    def _get_register_client(self, channel): #  不再需要这个方法，直接在 register_async 中创建 Stub
        """
        获取注册客户端的占位符方法。
        已更新为直接在 register_async 中创建 Stub。
        """
        pass #  不再需要

    def _create_register_request(self): #  不再需要这个方法，直接在 register_async 中创建 Request
        """
        创建注册请求的占位符方法。
        已更新为直接在 register_async 中创建 Request。
        """
        pass #  不再需要


    async def _execute_register_request(self, client, request): #  不再需要这个方法，直接在 register_async 中调用 client.Register
        """
        执行注册请求的占位符方法。
        已更新为直接在 register_async 中调用 client.Register。
        """
        pass #  不再需要

    def _command_connection_alive_timer_tick(self):
        """
        命令连接心跳定时器触发时的处理方法。
        """
        asyncio.create_task(self._async_command_connection_alive_timer_tick()) # 使用 asyncio.create_task 运行异步心跳

    async def _async_command_connection_alive_timer_tick(self):
        """
        异步命令连接心跳定时器触发时的处理方法。
        """
        try:
            if self.command_listening_call is None:
                raise Exception("CommandListeningCall is None!")
            if self.command_listening_call_cancellation_token_source: # 检查是否取消
                return
            # self.logger.debug("向命令流发送心跳包。")
            await self._send_heartbeat() # 发送心跳
        except Exception as exception:
            self.logger.error(exception, "命令流与集控服务器断开。")
            self.command_listening_call_cancellation_token_source = True # 设置取消标志
            self._stop_command_alive_timer() # 停止定时器
            self.command_listening_call = None
            self.logger.info("尝试重新连接命令流")
            self.listen_commands() # 重新监听命令

    async def _send_heartbeat(self):
        """
        发送心跳包。
        使用 gRPC 流来发送心跳请求 (Ping 命令)。
        """
        try:
            request = ClientCommandDeliverScReq_pb2.ClientCommandDeliverScReq(type=CommandTypes.Ping) # 创建 Ping 请求
            await self.command_listening_call.RequestStream.write(request) # 使用 await
            print("gRPC Stream: 发送心跳包 Ping")
        except grpc.RpcError as e:
            self.logger.error(f"发送心跳包失败: {e.details()}", exc_info=True)
            raise


    def _stop_command_alive_timer(self):
        """
        停止命令心跳定时器。
        您需要实现定时器停止逻辑，如果使用了 Python 的定时器库。
        """
        # TODO: 停止定时器 (如果使用 threading.Timer, 需要考虑如何安全停止)
        print("Timer: 停止心跳定时器 (threading.Timer 需要手动管理停止)")
        pass #  如果使用 threading.Timer，需要更复杂的停止机制


    async def listen_commands(self):
        """
        监听来自集控服务器的命令。
        使用 gRPC 双向流进行通信 (ClientCommandDeliver 服务)。
        """
        if self.command_listening_call is not None:
            self.logger.warning("已连接到命令流，无需重复连接")
            return
        try:
            self.logger.info("正在连接到命令流")
            client = ClientCommandDeliver_pb2_grpc.ClientCommandDeliverStub(self.channel) # 获取命令投递客户端 Stub
            metadata = self._create_metadata() # 创建 metadata
            call = client.ListenCommand(metadata=metadata) # 启动命令流 (异步调用)
            self.command_listening_call_cancellation_token_source = False # 重置取消标志
            self.command_listening_call = call
            self._start_command_alive_timer() # 启动心跳定时器
            # await call.RequestStream.WriteAsync(new ClientCommandDeliverScReq()) # 初始写入，C# 代码中有，Python gRPC 是否需要待确认

            async for response in call: # 异步迭代接收响应
                if self.command_listening_call_cancellation_token_source: # 检查取消状态
                    break # 如果取消，则退出循环
                if response is None:
                    continue
                command_type = CommandTypes(response.type) # 将枚举数值转换为 CommandTypes 枚举
                if command_type == CommandTypes.Pong: # 处理 Pong 回复
                    continue

                if response.retCode != Retcode.Success:
                    self.logger.warning(f"接受指令时未返回成功代码：{Retcode(response.retCode).name}") # 使用 Retcode 枚举的 name 属性
                    continue
                self.logger.info(f"接受指令：[{CommandTypes(response.type).name}] {response.payload.decode()}") # 使用 CommandTypes 枚举的 name 属性, 并解码 payload
                self._handle_command_received(response) # 处理接收到的命令

        except grpc.RpcError as ex: # 捕获 gRPC 异常
            if ex.code() == grpc.StatusCode.CANCELLED: # 忽略取消异常，属于正常关闭
                self.logger.info("命令流连接已取消 (正常关闭).")
                return
            self.logger.error(f"无法连接到集控服务器命令流，将在30秒后重试。Error: {ex.details()}, Code: {ex.code().name}", exc_info=True) # 打印详细错误信息和 gRPC 状态码
            self._stop_command_alive_timer() # 停止心跳定时器
            self.command_listening_call = None
            self._schedule_reconnect() # 计划重连
        except Exception as ex: # 捕获其他异常
            self.logger.error(ex, "连接命令流时发生非 gRPC 异常，将在30秒后重试。")
            self._stop_command_alive_timer() # 停止心跳定时器
            self.command_listening_call = None
            self._schedule_reconnect() # 计划重连


    def _get_command_deliver_client(self, channel): #  不再需要这个方法，直接在 listen_commands 中创建 Stub
        """
        获取命令投递客户端的占位符方法。
        已更新为直接在 listen_commands 中创建 Stub。
        """
        pass #  不再需要

    def _create_metadata(self):
        """
        创建 gRPC Metadata。
        包含 "cuid" (客户端唯一 ID) 在 Metadata 中发送。
        """
        metadata = [('cuid', self.client_guid)] # 创建 Metadata 列表
        print(f"gRPC Metadata: 创建包含 cuid: {self.client_guid}")
        return metadata # 返回 Metadata 对象


    def _start_command_stream(self, client, metadata): #  不再需要这个方法，直接在 listen_commands 中调用 client.ListenCommand
        """
        启动 gRPC 命令流的占位符方法。
        已更新为直接在 listen_commands 中调用 client.ListenCommand。
        """
        pass #  不再需要


    async def _receive_command_response(self, call): #  不再需要这个方法，直接在 listen_commands 中异步迭代 call
        """
        接收命令响应的占位符方法。
        已更新为直接在 listen_commands 中异步迭代 call。
        """
        pass #  不再需要


    def _start_command_alive_timer(self):
        """
        启动命令心跳定时器。
        使用 threading.Timer 定期触发 _command_connection_alive_timer_tick 方法。
        """
        print("Timer: 启动心跳定时器")
        def timer_callback():
            self._command_connection_alive_timer_tick() # 调用异步心跳触发方法
            if not self.command_listening_call_cancellation_token_source: # 如果未取消，则重新设置定时器
                self.timer = threading.Timer(self.command_connection_alive_timer_interval, timer_callback) # 重新创建 Timer 对象
                self.timer.daemon = True # 设置为守护线程
                self.timer.start() # 启动新的 Timer

        import threading
        self.timer = threading.Timer(self.command_connection_alive_timer_interval, timer_callback) # 创建 Timer 对象
        self.timer.daemon = True # 设置为守护线程
        self.timer.start() # 启动定时器


    def _handle_command_received(self, response):
        """
        处理接收到的命令。
        根据命令类型执行相应的操作，并触发 CommandReceived 事件。
        """
        # TODO: 根据 response.type 处理命令
        command_type = CommandTypes(response.type) # 获取 CommandTypes 枚举
        print(f"Command Handling: 处理命令 {command_type.name}") # 使用枚举 name 属性
        if command_type == CommandTypes.RestartApp:
            self._restart_app_command() # 调用重启应用命令方法
        elif command_type == CommandTypes.SendNotification: # 处理 SendNotification 命令
            self._handle_send_notification_command(response.payload) # 处理通知命令
        if self.command_received_event: # 触发事件
            event_args = ClientCommandEventArgs(type=command_type, payload=response.payload.decode()) # 创建事件参数，并解码 payload
            for handler in self.command_received_event: # 遍历事件处理函数列表
                handler(self, event_args) # 调用事件处理函数

    def _handle_send_notification_command(self, payload_bytes):
        """
        处理 SendNotification 命令。
        解析 Payload 并执行发送通知的操作。
        """
        try:
            send_notification_command = SendNotification_pb2.SendNotification() # 导入并创建 SendNotification 消息对象
            send_notification_command.ParseFromString(payload_bytes) # 解析 Payload
            print(f"Send Notification Command Received: {send_notification_command}") # 打印通知命令内容
            # TODO: 在这里实现显示通知的具体逻辑 (例如调用操作系统的通知 API)
            pass #  实现显示通知的逻辑
        except Exception as e:
            self.logger.error(f"处理 SendNotification 命令 Payload 失败: {e}", exc_info=True)


    def _restart_app_command(self):
        """
        处理重启应用命令的占位符方法。
        您需要实现应用重启的逻辑。
        """
        # TODO: 实现应用重启逻辑
        print("App Restart Command: 执行应用重启")
        self._restart_app(True) # 调用重启应用方法

    def _restart_app(self, force_restart=False):
        """
        重启应用的占位符方法。
        您需要实现应用重启的逻辑。
        """
        # TODO: 实现应用重启逻辑
        print("App Restart: 应用重启")
        pass # 执行应用重启操作

    def _schedule_reconnect(self):
        """
        计划重连。
        设置一个定时器，在 30 秒后尝试重新连接 (调用 listen_commands)。
        """
        print("Reconnect: 30秒后尝试重连")
        def reconnect_callback():
            asyncio.run(self.listen_commands()) # 使用 asyncio.run 运行异步 listen_commands

        import threading
        threading.Timer(30, reconnect_callback).start()


    async def get_manifest(self):
        """
        获取集控清单。
        从预定义的 Manifest URL 发起 HTTP GET 请求。
        """
        manifest_url = self.manifest_url
        self.logger.info(f"发起json请求：{manifest_url}")
        return await self._web_request_get_json(manifest_url, ManagementManifest) # 使用 web_request_helper 获取 json

    async def _web_request_get_json(self, url, response_type):
        """
        发起 Web 请求获取 JSON 数据。
        您需要使用 HTTP 客户端库（如 aiohttp）来实现异步请求。
        """
        import aiohttp # 导入 aiohttp
        print(f"Web Request: GET {url}, 返回 {response_type.__name__}")
        try:
            async with aiohttp.ClientSession() as session: # 使用 async with 创建 session
                async with session.get(url) as response: # 异步 GET 请求
                    if response.status == 200:
                        data = await response.json() # 异步解析 JSON
                        if response_type == ManagementManifest:
                            manifest = ManagementManifest()
                            manifest.__dict__.update(data)
                            return manifest # 返回 ManagementManifest 对象
                        elif response_type == dict: #  如果期望返回字典
                            return data
                        else: #  其他类型，您可能需要根据实际情况扩展
                            return data #  返回原始数据
                    else:
                        self.logger.error(f"Web 请求失败，URL: {url}, 状态码: {response.status}")
                        return None #  请求失败返回 None
        except aiohttp.ClientError as e: # 捕获 aiohttp 客户端异常
            self.logger.error(f"Web 请求异常，URL: {url}, 异常: {e}", exc_info=True)
            return None

    def decorate_url(self, url):
        """
        装饰 URL，替换占位符 {cuid}, {id}, {host}。
        """
        decorated_url = url.replace("{cuid}", self.client_guid).replace("{id}", self.id).replace("{host}", self.host)
        self.logger.debug(f"拼接url模板：{url} -> {decorated_url} ")
        return decorated_url

    async def get_json_async(self, url):
        """
        发起 GET 请求获取 JSON 数据。
        URL 会先经过 decorate_url 方法处理。
        """
        decorated_url = self.decorate_url(url)
        self.logger.info(f"发起json请求：{decorated_url}")
        return await self._web_request_get_json(decorated_url, dict) # 返回字典，您可以根据需要修改返回类型

    async def save_json_async(self, url, path):
        """
        发起 GET 请求获取 JSON 数据并保存到本地文件。
        URL 会先经过 decorate_url 方法处理。
        """
        decorated_url = self.decorate_url(url)
        self.logger.info(f"保存json请求：{decorated_url} {path}")
        policy_data = await self._web_request_get_json(decorated_url, dict) # 获取 JSON 数据
        if policy_data: # 确保数据获取成功
            return await self._save_json_to_file(policy_data, path, ManagementPolicy) # 保存到文件并返回 ManagementPolicy 对象
        else:
            return None #  数据获取失败返回 None


    async def _web_request_save_json(self, url, path, response_type): #  不再直接 web request save json，改为先 get json 再 save to file
        """
        发起 Web 请求获取 JSON 数据并保存到本地文件的占位符方法。
        已更新为先使用 _web_request_get_json 获取 JSON 数据，再调用 _save_json_to_file 保存。
        """
        pass #  不再需要

    async def _save_json_to_file(self, json_data, path, response_type):
        """
        将 JSON 数据保存到本地文件，并返回 response_type 的实例。
        """
        print(f"保存 JSON 到文件: {path}, 类型: {response_type.__name__}")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False) # 保存 JSON 数据到文件

            if response_type == ManagementPolicy: #  如果期望返回 ManagementPolicy 对象
                policy = ManagementPolicy()
                policy.__dict__.update(json_data) # 使用加载的数据更新 ManagementPolicy 对象
                return policy # 返回 ManagementPolicy 对象
            else: #  其他类型，您可能需要根据实际情况扩展
                return json_data #  返回原始 JSON 数据
        except Exception as e:
            self.logger.error(f"保存 JSON 到文件 {path} 失败: {e}", exc_info=True)
            return None


    def on_command_received(self, handler_function):
        """
        注册命令接收事件处理函数。
        可以注册多个处理函数。
        """
        if self.command_received_event is None:
            self.command_received_event = []
        self.command_received_event.append(handler_function)

    def close_connection(self):
        """
        关闭连接，停止命令监听和心跳。
        """
        self.logger.info("正在关闭管理服务器连接。")
        self.command_listening_call_cancellation_token_source = True # 设置取消标志
        self._stop_command_alive_timer() # 停止心跳定时器
        if self.command_listening_call and self.command_listening_call.RequestStream: # 尝试关闭 gRPC 双向流
            asyncio.run(self.command_listening_call.RequestStream.cancel()) # 尝试取消请求流 (Python gRPC 异步流可能不需要显式 cancel RequestStream)
            self._close_grpc_channel(self.channel) # 关闭 gRPC Channel
            self.channel = None
        self.command_listening_call = None

    def _close_grpc_channel(self, channel):
        """
        关闭 gRPC Channel。
        使用 grpc 库来关闭 Channel。
        """
        # TODO: 使用 gRPC 库关闭 Channel
        print("gRPC Channel: 关闭 gRPC Channel")
        if channel:
            asyncio.run(channel.close()) # 使用 asyncio.run to await channel.close() if it's async


class ServerlessConnection(ManagementServerConnectionInterface): # 模拟 C# ServerlessConnection
    """
    用于 Serverless 集控模式的连接类。
    主要通过 HTTP 请求获取 Manifest，不使用 gRPC。
    """
    def __init__(self, client_uid, class_identity, manifest_url_template):
        """
        初始化 ServerlessConnection 实例。

        Args:
            client_uid (str): 客户端唯一 ID。
            class_identity (str): 客户端标识。
            manifest_url_template (str): Manifest URL 模板。
        """
        self.logger = self._get_logger()  # 需要您实现一个 logger 获取方法
        self.client_guid = client_uid
        self.id = class_identity
        self.manifest_url_template = manifest_url_template

    def _get_logger(self):
        """
        获取 logger 实例的占位符方法。
        您需要根据您的日志框架实现此方法。
        """
        #  TODO: 实现获取 logger 的逻辑
        print("Logger placeholder (Serverless): 请配置您的日志系统")
        class DummyLogger: #  一个简单的占位 logger
            def info(self, msg): print(f"INFO: {msg}")
            def warning(self, msg): print(f"WARNING: {msg}")
            def error(self, msg, exc_info=None, stack_info=False): print(f"ERROR: {msg}, Exception: {exc_info}") # 添加 stack_info 参数
            def debug(self, msg): print(f"DEBUG: {msg}")
        return DummyLogger()


    async def get_manifest(self):
        """
        获取集控清单。
        根据 manifest_url_template 拼接 URL 并发起 HTTP GET 请求。
        """
        manifest_url = self.manifest_url_template.replace("{cuid}", self.client_guid).replace("{id}", self.id)
        self.logger.info(f"发起json请求：{manifest_url}")
        return await self._web_request_get_json(manifest_url, ManagementManifest) # 使用 web_request_helper 获取 json

    async def _web_request_get_json(self, url, response_type):
        """
        发起 Web 请求获取 JSON 数据。
        您需要使用 HTTP 客户端库（如 aiohttp）来实现异步请求。
        """
        import aiohttp # 导入 aiohttp
        print(f"Web Request (Serverless): GET {url}, 返回 {response_type.__name__}")
        try:
            async with aiohttp.ClientSession() as session: # 使用 async with 创建 session
                async with session.get(url) as response: # 异步 GET 请求
                    if response.status == 200:
                        data = await response.json() # 异步解析 JSON
                        if response_type == ManagementManifest:
                            manifest = ManagementManifest()
                            manifest.__dict__.update(data)
                            return manifest # 返回 ManagementManifest 对象
                        elif response_type == dict: #  如果期望返回字典
                            return data
                        else: #  其他类型，您可能需要根据实际情况扩展
                            return data #  返回原始数据
                    else:
                        self.logger.error(f"Web 请求失败，URL: {url}, 状态码: {response.status}")
                        return None #  请求失败返回 None
        except aiohttp.ClientError as e: # 捕获 aiohttp 客户端异常
            self.logger.error(f"Web 请求异常，URL: {url}, 异常: {e}", exc_info=True)
            return None

    async def save_json_async(self, url, path):
        """
        发起 GET 请求获取 JSON 数据并保存到本地文件（Serverless 模式下可能不常用，但为了接口一致性保留）。
        """
        self.logger.warning("Serverless 模式下 save_json_async 方法可能不常用。")
        decorated_url = url.replace("{cuid}", self.client_guid).replace("{id}", self.id) # Serverless 模式不需要 decorate_url 方法中的 host
        self.logger.info(f"保存json请求：{decorated_url} {path}")
        policy_data = await self._web_request_get_json(decorated_url, dict) # 获取 JSON 数据
        if policy_data: # 确保数据获取成功
            return await self._save_json_to_file(policy_data, path, ManagementPolicy) # 保存到文件并返回 ManagementPolicy 对象
        else:
            return None #  数据获取失败返回 None

    async def _web_request_save_json(self, url, path, response_type): #  不再直接 web request save json，改为先 get json 再 save to file
        """
        发起 Web 请求获取 JSON 数据并保存到本地文件的占位符方法。
        已更新为先使用 _web_request_get_json 获取 JSON 数据，再调用 _save_json_to_file 保存。
        """
        pass #  不再需要

    async def _save_json_to_file(self, json_data, path, response_type):
        """
        将 JSON 数据保存到本地文件，并返回 response_type 的实例。
        """
        print(f"保存 JSON 到文件 (Serverless): {path}, 类型: {response_type.__name__}")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False) # 保存 JSON 数据到文件

                if response_type == ManagementPolicy: #  如果期望返回 ManagementPolicy 对象
                    policy = ManagementPolicy()
                    policy.__dict__.update(json_data) # 使用加载的数据更新 ManagementPolicy 对象
                    return policy # 返回 ManagementPolicy 对象
                else: #  其他类型，您可能需要根据实际情况扩展
                    return json_data #  返回原始 JSON 数据
        except Exception as e:
            self.logger.error(f"保存 JSON 到文件 {path} 失败: {e}", exc_info=True)
            return None


    async def register_async(self):
        """
        Serverless 模式下注册方法为空实现，因为不需要显式注册。
        """
        self.logger.warning("Serverless 模式下 register_async 方法为空实现。")
        return await self.get_manifest() # 直接返回 manifest

    async def get_json_async(self, url):
        """
        发起 GET 请求获取 JSON 数据（Serverless 模式）。
        """
        decorated_url = url.replace("{cuid}", self.client_guid).replace("{id}", self.id) # Serverless 模式不需要 decorate_url 方法中的 host
        self.logger.info(f"发起json请求 (Serverless): {decorated_url}")
        return await self._web_request_get_json(decorated_url, dict) # 返回字典，您可以根据需要修改返回类型

    def on_command_received(self, handler_function):
        """
        Serverless 模式下命令接收事件，通常 Serverless 模式不主动接收命令，可以用于模拟或扩展。
        """
        self.logger.warning("Serverless 模式下 on_command_received 事件通常不使用。")
        pass # Serverless 通常不主动接收命令

    def listen_commands(self):
        """
        Serverless 模式下监听命令方法为空实现，因为通常不主动监听命令。
        """
        self.logger.warning("Serverless 模式下 listen_commands 方法为空实现。")
        pass # Serverless 通常不主动监听命令

    def close_connection(self):
        """
        Serverless 模式下关闭连接方法为空实现。
        """
        self.logger.info("Serverless 模式下 close_connection 方法为空实现。")
        pass

class AuthorizeService: # 模拟 C# AuthorizeService
    """
    模拟授权服务，用于验证用户凭据。
    """
    async def authenticate_async(self, credential):
        """
        异步认证方法，验证提供的凭据。
        """
        # TODO: 实现实际的认证逻辑，例如与认证服务器通信或本地验证
        print(f"AuthorizeService placeholder: 认证凭据 '{credential}'")
        # 模拟认证结果，您可以根据实际情况修改模拟逻辑
        return credential == "valid_credential" # 模拟凭据 "valid_credential" 通过认证

class CommonDialog: # 模拟 C# CommonDialog
    """
    模拟通用对话框，用于显示信息或提示用户操作。
    """
    @staticmethod
    def show_info(message):
        """
        显示信息对话框。
        """
        print(f"CommonDialog Info: {message}")

    @staticmethod
    def show_dialog(builder):
        """
        显示通用对话框，并根据用户操作返回结果。
        """
        print(f"CommonDialog Show: {builder.content}, Actions: {builder.actions}")
        # 模拟用户点击 "加入" 或 "退出" 按钮，返回 1 表示确认，0 表示取消
        return 1 # 模拟用户点击确认


class CommonDialogBuilder: # 模拟 C# CommonDialogBuilder
    """
    模拟通用对话框构建器，用于创建和配置对话框。
    """
    def __init__(self):
        self.content = None
        self.icon_kind = None
        self.actions = [] #  [(action_name, is_default)]

    def set_content(self, content):
        """
        设置对话框内容。
        """
        self.content = content
        return self

    def set_icon_kind(self, icon_kind):
        """
        设置对话框图标类型。
        """
        self.icon_kind = icon_kind
        return self

    def add_cancel_action(self, action_name="取消"):
        """
        添加取消操作按钮。
        """
        self.actions.append((action_name, False))
        return self

    def add_action(self, action_name, icon_kind, is_default): # icon_kind 参数占位
        """
        添加自定义操作按钮。
        """
        self.actions.append((action_name, is_default))
        return self

    def show_dialog(self):
        """
        显示对话框，并返回用户操作结果。
        """
        return CommonDialog.show_dialog(self)


class ManagementService: # 模拟 C# ManagementService
    """
    集控管理服务类，负责集控功能的整体管理。
    包括配置加载、连接管理、命令处理、加入/退出集控等。
    """
    instance = None # 模拟 Instance 静态属性

    management_preset_path = "./ManagementPreset.json" # 示例路径
    management_configure_folder_path = "Management" # 示例路径
    local_management_configure_folder_path = "LocalManagement" # 示例路径

    management_persist_config_path = os.path.join(management_configure_folder_path, "Persist.json")
    management_manifest_path = os.path.join(management_configure_folder_path, "Manifest.json")
    management_versions_path = os.path.join(management_configure_folder_path, "Versions.json")
    management_settings_path = os.path.join(management_configure_folder_path, "Settings.json")
    management_policy_path = os.path.join(management_configure_folder_path, "Policy.json")

    local_management_policy_path = os.path.join(local_management_configure_folder_path, "Policy.json")
    local_management_credentials_path = os.path.join(local_management_configure_folder_path, "Credentials.json")

    def __init__(self, logger, authorize_service):
        """
        初始化 ManagementService 实例。
        """
        ManagementService.instance = self # 设置单例实例
        self.logger = logger
        self.authorize_service = authorize_service
        self.persist = self._load_config(ManagementService.management_persist_config_path, ManagementClientPersistConfig)
        self.settings = self._load_config(ManagementService.management_settings_path, ManagementSettings)
        self.is_management_enabled = self.settings.is_management_enabled

        if not self.is_management_enabled:
            return

        try:
            if self.settings.management_server_kind == ManagementServerKind.Serverless:
                self.connection = ServerlessConnection(self.persist.client_unique_id, self.settings.class_identity or "", self.settings.manifest_url_template)
            elif self.settings.management_server_kind == ManagementServerKind.ManagementServer:
                self.connection = ManagementServerConnection(self.settings, self.persist.client_unique_id, False)
            else:
                raise ValueError("无效的集控服务器类型。")
            self.connection.on_command_received(self._connection_on_command_received) # 注册命令接收事件处理函数
        except Exception as ex:
            self.logger.error(f"连接集控服务器失败: {ex}", exc_info=True)
            self.connection = None # 连接失败时将 connection 设置为 None


    @staticmethod
    def init_management():
        """
        静态初始化方法，目前为空实现。
        """
        pass #  目前为空实现

    @staticmethod
    def get_instance():
        """
        获取 ManagementService 的单例实例。
        """
        return ManagementService.instance

    def _load_config(self, path, config_type):
        """
        加载配置文件的占位符方法。
        您需要实现从 JSON 文件加载配置的逻辑。
        """
        # TODO: 从 JSON 文件加载配置
        print(f"Config Load placeholder: 加载 {config_type.__name__} from {path}")
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if config_type == ManagementSettings:
                        settings = ManagementSettings()
                        settings.__dict__.update(data) # 简单地用字典更新对象属性
                        return settings
                    elif config_type == ManagementManifest:
                        manifest = ManagementManifest()
                        manifest.__dict__.update(data)
                        return manifest
                    elif config_type == ManagementPolicy:
                        policy = ManagementPolicy()
                        policy.__dict__.update(data)
                        return policy
                    elif config_type == ManagementVersions:
                        versions = ManagementVersions()
                        versions.__dict__.update(data)
                        return versions
                    elif config_type == ManagementCredentialConfig:
                        credential_config = ManagementCredentialConfig()
                        credential_config.__dict__.update(data)
                        return credential_config
                    elif config_type == ManagementClientPersistConfig:
                        persist_config = ManagementClientPersistConfig()
                        persist_config.__dict__.update(data)
                        return persist_config
                    else:
                        return config_type() # 返回默认实例
            except json.JSONDecodeError:
                print(f"JSONDecodeError: 无法解析文件 {path}")
                return config_type() # 解析失败返回默认实例
        else:
            return config_type() # 文件不存在返回默认实例


    def _connection_on_command_received(self, sender, event_args):
        """
        命令接收事件处理方法。
        根据命令类型执行相应的操作。
        """
        if event_args.type == CommandTypes.RestartApp:
            self._restart_app_command() # 处理重启应用命令
        elif event_args.type == CommandTypes.SendNotification: # 处理 SendNotification 命令
            self._handle_send_notification_command(event_args.payload) # 处理通知命令

    def _handle_send_notification_command(self, payload_bytes):
        """
        处理 SendNotification 命令。
        解析 Payload 并执行发送通知的操作。
        """
        try:
            send_notification_command = SendNotification_pb2.SendNotification() # 导入并创建 SendNotification 消息对象
            if payload_bytes: # 检查 payload_bytes 是否为空
                send_notification_command.ParseFromString(payload_bytes) # 解析 Payload
            print(f"Send Notification Command Received: {send_notification_command}") # 打印通知命令内容
            # TODO: 在这里实现显示通知的具体逻辑 (例如调用操作系统的通知 API)
            pass #  实现显示通知的逻辑
        except Exception as e:
            self.logger.error(f"处理 SendNotification 命令 Payload 失败: {e}", exc_info=True)


    def _restart_app_command(self):
        """
        处理重启应用命令的占位符方法。
        您需要实现应用重启的逻辑。
        """
        # TODO: 实现应用重启逻辑
        print("App Restart Command placeholder: 执行应用重启")
        self._restart_app(True) # 调用重启应用方法

    def _restart_app(self, force_restart=False):
        """
        重启应用的占位符方法。
        您需要实现应用重启的逻辑。
        """
        # TODO: 实现应用重启逻辑
        print("App Restart placeholder: 应用重启")
        pass # 执行应用重启操作


    def _setup_local_management(self):
        """
        设置本地集控配置，在未加入集控时使用本地策略和凭据。
        """
        self.policy = self._load_config(ManagementService.local_management_policy_path, ManagementPolicy)
        self.credential_config = self._load_config(ManagementService.local_management_credentials_path, ManagementCredentialConfig)

        #  Python 中属性的修改不需要像 C# 那样手动绑定事件，直接修改属性即可

    async def setup_management(self):
        """
        初始化集控，加载集控配置和策略。
        如果未启用集控，则设置本地集控。
        """
        if not self.is_management_enabled:
            self._setup_local_management()
            return

        self.logger.info("正在初始化集控")
        self.manifest = self._load_config(ManagementService.management_manifest_path, ManagementManifest)
        self.policy = self._load_config(ManagementService.management_policy_path, ManagementPolicy)
        self.versions = self._load_config(ManagementService.management_versions_path, ManagementVersions)

        if self.connection is None: #  处理连接初始化失败的情况
            self.logger.warning("集控连接未建立，跳过清单和策略拉取。")
            return

        try:
            self.manifest = await self.connection.get_manifest()
            self._save_config(ManagementService.management_manifest_path, self.manifest)

            if self.manifest.policy_source and (not self.versions.policy_version or self._is_newer_version(self.manifest.policy_source, self.versions.policy_version)):
                self.policy = await self.connection.save_json_async(self.manifest.policy_source, ManagementService.management_policy_path)
                self.versions.policy_version = self.manifest.policy_source #  假设 policy_source 可以作为版本标识
        except Exception as e:
            self.logger.error(e, "拉取集控清单与策略失败")

    def _is_newer_version(self, version_a, version_b):
        """
        比较版本是否更新的占位符方法。
        您需要根据实际的版本比较逻辑来实现。
        这里简单地比较字符串，实际应用中可能需要更复杂的版本号解析和比较。
        """
        # TODO: 实现版本比较逻辑
        print(f"Version Compare placeholder: 比较版本 {version_a} vs {version_b}")
        if not version_b: # 如果 version_b 为空，则 a 更新
            return True
        return version_a != version_b # 简单字符串比较，实际应用中可能需要更复杂的版本号解析

    def save_settings(self):
        """
        保存集控配置，例如版本信息。
        """
        self.logger.info("保存集控配置")
        self._save_config(ManagementService.management_versions_path, self.versions)

    def _save_config(self, path, config_object):
        """
        保存配置到 JSON 文件的占位符方法。
        您需要实现将配置对象序列化为 JSON 并保存到文件的逻辑。
        """
        # TODO: 将配置对象保存到 JSON 文件
        print(f"Config Save placeholder: 保存 {config_object.__class__.__name__} to {path}")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(config_object.__dict__, f, indent=4, ensure_ascii=False) # 简单地将对象属性字典转为 JSON
        except Exception as e:
            self.logger.error(f"保存配置到 {path} 失败: {e}", exc_info=True)


    async def join_management_async(self, settings):
        """
        加入集控。
        根据提供的集控设置连接集控服务器，获取 Manifest，并提示用户确认加入。
        """
        if self.is_management_enabled:
            raise Exception("无法在已加入管理后再次加入管理。")
        mf = ManagementManifest()
        try:
            if settings.management_server_kind == ManagementServerKind.Serverless:
                mf = await self.connection._web_request_get_json(settings.manifest_url_template, ManagementManifest) # 直接使用 connection 的 _web_request_get_json
            elif settings.management_server_kind == ManagementServerKind.ManagementServer:
                connection = ManagementServerConnection(settings, self.persist.client_unique_id, True) # 轻量连接，仅用于注册
                mf = await connection.register_async()
                connection.close_connection() # 关闭临时连接
            else:
                raise ValueError("无效的服务器类型。")
        except Exception as e:
            self.logger.error(f"加入集控时获取 Manifest 失败: {e}", exc_info=True)
            raise

        dialog_builder = CommonDialogBuilder()
        dialog_builder.set_content(f"确定要加入组织 {mf.organization_name} 的管理吗？")
        dialog_builder.set_icon_kind("Hint") #  PackIconKind.Hint 对应的图标类型
        dialog_builder.add_cancel_action()
        dialog_builder.add_action("加入", "Check", True) # PackIconKind.Check 对应的图标类型

        result = CommonDialog.show_dialog(dialog_builder) # CommonDialog.show_dialog 返回模拟的用户选择
        if result != 1: # 1 代表 "加入"
            return

        w = ManagementSettings() # 创建新的 ManagementSettings 对象
        w.__dict__.update(settings.__dict__) # 复制 settings 的属性
        w.is_management_enabled = True

        # 清空旧的配置 (模拟文件删除)
        files_to_delete = [
            ManagementService.management_manifest_path,
            ManagementService.management_policy_path,
            ManagementService.management_versions_path,
            # ProfileService.management_class_plan_path, #  ProfileService 在 Python 代码中未定义，需要您根据实际情况添加或移除
            # ProfileService.management_subjects_path,
            # ProfileService.management_time_layout_path,
            "./Profiles/_management-profile.json" # 示例路径，需要根据实际情况调整
        ]
        for file_path in files_to_delete:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    if os.path.exists(file_path + ".bak"): # 模拟 .bak 文件删除
                        os.remove(file_path + ".bak")
                    print(f"删除文件: {file_path}")
                except OSError as e:
                    self.logger.warning(f"删除文件 {file_path} 失败: {e}")


        self._save_config(ManagementService.management_settings_path, w)
        CommonDialog.show_info(f"已加入组织 {mf.organization_name} 的管理。应用将重启以应用更改。")

        self._restart_app() # 重启应用


    async def exit_management_async(self):
        """
        退出集控。
        需要进行权限认证，并检查策略是否允许退出。
        """
        if not self.is_management_enabled:
            raise Exception("无法在没有加入集控的情况下退出集控。")
        auth_result = await self.authorize_by_level(self.credential_config.exit_management_authorize_level)
        if not auth_result:
            raise Exception("认证失败。")
        if not self.policy.allow_exit_management:
            raise Exception("您的组织不允许您退出集控。")

        dialog_builder = CommonDialogBuilder()
        dialog_builder.set_content(f"确定要退出组织 {self.manifest.organization_name} 的管理吗？")
        dialog_builder.set_icon_kind("Hint") #  CommonDialogIconKind.Hint 对应的图标类型
        dialog_builder.add_cancel_action()
        dialog_builder.add_action("退出", "ExitRun", True) # PackIconKind.ExitRun 对应的图标类型

        result = CommonDialog.show_dialog(dialog_builder) # CommonDialog.show_dialog 返回模拟的用户选择
        if result != 1: # 1 代表 "退出"
            return

        self.settings.is_management_enabled = False
        self._save_config(ManagementService.management_settings_path, self.settings)

        CommonDialog.show_info(f"已退出组织 {self.manifest.organization_name} 的管理。应用将重启以应用更改。")

        self._restart_app() # 重启应用

    async def authorize_by_level(self, level):
        """
        根据权限级别进行认证。
        """
        if not self.credential_config.admin_credential and not self.credential_config.user_credential:
            return True

        fallback_credential = next((c for c in [self.credential_config.admin_credential, self.credential_config.user_credential] if c), None) # 模拟 C# FirstOrDefault

        def fallback(c):
            return c if c else fallback_credential

        if level == AuthorizeLevel.NoneLevel:
            return True
        elif level == AuthorizeLevel.User:
            credential = fallback(self.credential_config.user_credential)
            return await self.authorize_service.authenticate_async(credential)
        elif level == AuthorizeLevel.Admin:
            credential = fallback(self.credential_config.admin_credential)
            return await self.authorize_service.authenticate_async(credential)
        else:
            raise ValueError(f"无效的权限级别: {level}")