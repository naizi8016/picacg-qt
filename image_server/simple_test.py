#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的测试脚本 - 使用Python内置库测试图片服务器
"""

import urllib.request
import urllib.error


def test_server():
    """使用urllib测试图片服务器"""
    base_url = "http://localhost:9180"

    # 测试不同的路径
    test_paths = ["/", "/test.jpg", "/api/image"]

    print("开始测试图片服务器...")
    print(f"服务器地址: {base_url}")
    print("-" * 50)

    for path in test_paths:
        url = base_url + path
        try:
            print(f"测试路径: {path}")

            # 发送请求
            with urllib.request.urlopen(url, timeout=5) as response:
                status_code = response.getcode()
                content_type = response.headers.get("Content-Type", "unknown")
                content_length = len(response.read())

                print(f"  ✓ 成功 - 状态码: {status_code}")
                print(f"  ✓ Content-Type: {content_type}")
                print(f"  ✓ 内容大小: {content_length} 字节")

                # 检查是否为图片数据
                if content_type.startswith("image/"):
                    print(f"  ✓ 返回的是图片数据")
                else:
                    print(f"  ⚠ 警告: 返回的不是图片数据")

            print()

        except urllib.error.URLError as e:
            print(f"  ✗ 请求失败: {e}")
            print()
        except Exception as e:
            print(f"  ✗ 发生错误: {e}")
            print()

    print("测试完成!")


if __name__ == "__main__":
    test_server()
