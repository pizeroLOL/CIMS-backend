# 基于 Python 的适用于 [ClassIsland](https://github.com/classisland/classisland) 的集控服务器

集控服务器分为三个部分，分别是[`api`](./ManagementServer/api.py)[`command`](./ManagementServer/command.py)[`gRPC`](./ManagementServer/gRPC.py)，分别用于：

| 组件 | [`api`](./ManagementServer/api.py)   | [`command`](./ManagementServer/command.py) | [`gRPC`](./ManagementServer/gRPC.py) |
|----|--------------------------------------|--------------------------------------------|--------------------------------------|
| 用途 | 向客户端分发配置文件                           | 通过API以集控服务器为中介获取客户端状态、向客户端发送指令             | 与客户端建立gRPC链接                         |
| 端口 | [50050](http://127.0.0.1:50050/docs) | [50052](http://127.0.0.1:50052/docs)       | 50051                                |

你可以直接启动 [`main.py`](./main.py)，本地测试用例请到 [`Notebook`](./ServerPresentation.ipynb) 中写入配置文件并启动服务器。

***项目仍在建设过程中，如有疑问、需求请提 [commit](https://github.com/kaokao221/ClassIslandManagementServer.py/issues/new)，可以提交 [PR](https://github.com/kaokao221/ClassIslandManagementServer.py/compare)***

***由于 ClassIsland 本身集控并未完工，服务器侧的刷新配置文件无法在发行版中生效，请注意***

***当前配置文件对接方式使用 `{client_uid}.json` 保存在 [`Datas`](./Datas) 目录下，请手动处理，自动化管理将在晚些时候完成***

## Star 历史
[![Stargazers over time](https://starchart.cc/kaokao221/ClassIslandManagementServer.py.svg?variant=adaptive)](https://starchart.cc/kaokao221/ClassIslandManagementServer.py)
