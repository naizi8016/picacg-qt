#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图片服务器的客户端脚本
"""

import requests
import time


def test_server():
    """测试图片服务器"""
    base_url = "http://localhost:9180"

    # 测试不同的路径
    test_paths = ["/", "/image.jpg", "/any/path/test.png", "/api/v1/image"]

    print("开始测试图片服务器...")
    print(f"服务器地址: {base_url}")
    print("-" * 50)

    for path in test_paths:
        url = base_url + path
        try:
            print(f"测试路径: {path}")
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "unknown")
                content_length = len(response.content)
                print(f"  ✓ 成功 - 状态码: {response.status_code}")
                print(f"  ✓ Content-Type: {content_type}")
                print(f"  ✓ 内容大小: {content_length} 字节")

                # 检查是否为图片数据
                if content_type.startswith("image/"):
                    print(f"  ✓ 返回的是图片数据")
                else:
                    print(f"  ⚠ 警告: 返回的不是图片数据")
            else:
                print(f"  ✗ 失败 - 状态码: {response.status_code}")
                print(f"  ✗ 错误信息: {response.text}")

            print()

        except requests.exceptions.RequestException as e:
            print(f"  ✗ 请求失败: {e}")
            print()

    print("测试完成!")


if __name__ == "__main__":
    # 等待服务器启动
    print("等待服务器启动...")
    time.sleep(2)

    test_server()
