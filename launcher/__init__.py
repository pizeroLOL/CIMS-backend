# -*- coding: utf-8 -*-
# ClassIslandManagementServer/launcher.py
import asyncio

from aiohttp import web

from ClassIslandManagementServer.client.ManagementServerConnection import create_app

def run_server():
    asyncio.run(create_app())

if __name__ == '__main__':
    run_server()
