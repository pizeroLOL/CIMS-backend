# 基于 Python 的适用于 [ClassIsland](https://github.com/classisland/classisland) 的集控服务器

集控服务器分为四个部分，分别是[`api`](./ManagementServer/api.py)[`command`](./ManagementServer/command.py)[`gRPC`](./ManagementServer/gRPC.py)[`WebUI`](./webui/README.md)，分别用于：

| 组件 | [`api`](./ManagementServer/api.py)   | [`command`](./ManagementServer/command.py) | [`gRPC`](./ManagementServer/gRPC.py) | [`WebUI`](./webui/README.md)     |
|----|--------------------------------------|--------------------------------------------|--------------------------------------|----------------------------------|
| 用途 | 向客户端分发配置文件                           | 通过API以集控服务器为中介获取客户端状态、向客户端发送指令             | 与客户端建立gRPC链接                         | 集控服务器网页前端（同时用作端口转发）              |
| 端口 | [50050](http://127.0.0.1:50050/docs) | [50052](http://127.0.0.1:50052/docs)       | 50051                                | [50053](http://127.0.0.1:50053/) |

## 配置

运行 `python -m pip install -r requirements.txt` 以安装依赖

运行 `python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. ./Protobuf/Client/ClientCommandDeliverScReq.proto ./Protobuf/Client/ClientRegisterCsReq.proto ./Protobuf/Command/HeartBeat.proto ./Protobuf/Command/SendNotification.proto ./Protobuf/Enum/CommandTypes.proto ./Protobuf/Enum/Retcode.proto ./Protobuf/Server/ClientCommandDeliverScRsp.proto ./Protobuf/Server/ClientRegisterScRsp.proto ./Protobuf/Service/ClientCommandDeliver.proto ./Protobuf/Service/ClientRegister.proto` 以编译 `.proto` 文件

现在，你可以直接启动 [`main.py`](./main.py)，也可以到到 [`Notebook`](./ServerPresentation.ipynb) 阅读一些其它的相关信息。

> ***项目仍在建设过程中，如有疑问、需求请提 [commit](https://github.com/kaokao221/ClassIslandManagementServer.py/issues/new)，可以提交 [PR](https://github.com/kaokao221/ClassIslandManagementServer.py/compare)***
> 
> ***由于 [ClassIsland](https://github.com/classisland/classisland) 本身集控并未完工，服务器侧的刷新配置文件无法在发行版中生效，请注意***
>
> ***当前配置文件对接方式发生变更，相关的管理晚些时候上线***

## WebUI

请先 `cd webui`，在执行下面的命令之前

运行 `npm install` 安装依赖

运行 `nmp run build` 构建生产环境的服务器

当前 WebUI 已经实现：
- [x] **概览页面**用于快速展示服务器已经注册的设备数量和在线的设备数量
- [x] **设备管理**用于向设备执行重启、推送消息和更新数据(更新数据客户端当前不支持，最早将在 1.7 版本上线)
- [ ] **配置文件管理**目前只实现基础的查看能力
- [ ] **设置**空的（

## ~~罢工了~~

## Star 历史
[![Stargazers over time](https://starchart.cc/kaokao221/ClassIslandManagementServer.py.svg?variant=adaptive)](https://starchart.cc/kaokao221/ClassIslandManagementServer.py)
