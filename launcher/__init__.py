# -*- coding: utf-8 -*-
# ClassIslandManagementServer/launcher.py
import asyncio
import logging
from aiohttp import web

from ManagementServerConnection import create_app

async def main():
    """主运行函数，启动 aiohttp app 和 gRPC 服务器."""
    app = await create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 50050) # 显式指定 host 和 port
    await site.start()
    logging.info(f"HTTP服务已启动，监听端口: {site.name}")
    # 保持服务器运行直到手动停止
    await asyncio.Future()

def run_server():
    """启动服务器的入口函数，使用 asyncio.run 运行主函数."""
    asyncio.run(main())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # 修改日志级别为 INFO，减少 DEBUG 输出
    run_server()