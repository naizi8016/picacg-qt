#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片服务器启动脚本
"""

from server import run_server

if __name__ == "__main__":
    # 可以在这里修改服务器配置
    HOST = "localhost"  # 服务器地址，可以改为 '0.0.0.0' 允许外部访问
    PORT = 9180  # 服务器端口

    run_server(host=HOST, port=PORT)
