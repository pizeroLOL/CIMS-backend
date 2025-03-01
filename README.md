# 基于 Python 的适用于 [ClassIsland](https://github.com/classisland/classisland) 的集控服务器

集控服务器分为四个部分，分别是[`api`](./ManagementServer/api.py)[`command`](./ManagementServer/command.py)[`gRPC`](./ManagementServer/gRPC.py)[`WebUI`](./webui/README.md)，分别用于：

| 组件 | [`api`](./ManagementServer/api.py)   | [`command`](./ManagementServer/command.py) | [`gRPC`](./ManagementServer/gRPC.py) | [`WebUI`](./webui/README.md)     |
|----|--------------------------------------|--------------------------------------------|--------------------------------------|----------------------------------|
| 用途 | 向客户端分发配置文件                           | 通过API以集控服务器为中介获取客户端状态、向客户端发送指令             | 与客户端建立gRPC链接                         | 集控服务器网页前端（同时用作端口转发）              |
| 端口 | [50050](http://127.0.0.1:50050/docs) | [50052](http://127.0.0.1:50052/docs)       | 50051                                | [50053](http://127.0.0.1:50053/) |

## 配置

运行 `python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. .\Protobuf\Client\*.proto .\Protobuf\Command\*.proto .\Protobuf\Enum\*.proto .\Protobuf\Server\*.proto .\Protobuf\Service\*.proto` 以编译 `.proto` 文件

运行 `python -m pip install -r requirements.txt` 以安装依赖

现在，你可以直接启动 [`main.py`](./main.py)，也可以到到 [`Notebook`](./ServerPresentation.ipynb) 阅读一些其它的相关信息。

> ***项目仍在建设过程中，如有疑问、需求请提 [commit](https://github.com/kaokao221/ClassIslandManagementServer.py/issues/new)，可以提交 [PR](https://github.com/kaokao221/ClassIslandManagementServer.py/compare)***
> 
> ***由于 [ClassIsland](https://github.com/classisland/classisland) 本身集控并未完工，服务器侧的刷新配置文件无法在发行版中生效，请注意***
>
> ***当前配置文件对接方式发生变更，相关的管理晚些时候上线***

## Star 历史
[![Stargazers over time](https://starchart.cc/kaokao221/ClassIslandManagementServer.py.svg?variant=adaptive)](https://starchart.cc/kaokao221/ClassIslandManagementServer.py)
