#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的图片服务器
对于所有请求都返回程序生成的随机图片
支持HTTP和HTTPS协议
"""

import os
import ssl
import random
import io
import ipaddress
from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes
from datetime import datetime


def generate_random_image():
    """生成随机程序化图片"""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        # 如果没有PIL库，生成简单的位图
        return generate_simple_bitmap()
    
    # 随机尺寸：宽度和高度独立变化，基准1080px ± 0-540px
    base_width = 1080
    base_height = 1080
    
    # 宽度和高度独立随机变化
    width_variation = random.randint(0, 540)
    height_variation = random.randint(0, 540)
    
    width = base_width + random.choice([-1, 1]) * width_variation
    height = base_height + random.choice([-1, 1]) * height_variation
    
    # 确保在540-1620px范围内
    width = max(540, min(1620, width))
    height = max(540, min(1620, height))
    
    # 创建图片
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    # 随机背景色
    bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    draw.rectangle([0, 0, width, height], fill=bg_color)
    
    # 添加程序化纹理
    num_shapes = random.randint(5, 20)
    for _ in range(num_shapes):
        shape_type = random.choice(['circle', 'rectangle', 'line'])
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        if shape_type == 'circle':
            x = random.randint(0, width)
            y = random.randint(0, height)
            radius = random.randint(10, min(width, height) // 4)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color, outline=color)
        
        elif shape_type == 'rectangle':
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(x1, min(width, x1 + random.randint(20, 200)))
            y2 = random.randint(y1, min(height, y1 + random.randint(20, 200)))
            draw.rectangle([x1, y1, x2, y2], fill=color, outline=color)
        
        elif shape_type == 'line':
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line([x1, y1, x2, y2], fill=color, width=random.randint(1, 5))
    
    # 添加时间戳和随机种子信息确保相对唯一性
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    seed_info = f"{random.randint(1000, 9999)}"
    text = f"{timestamp} | {seed_info}"
    
    try:
        # 尝试添加文字（如果字体可用）
        text_color = (255 - bg_color[0], 255 - bg_color[1], 255 - bg_color[2])
        draw.text((10, 10), text, fill=text_color)
    except:
        pass
    
    # 保存到内存
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def generate_simple_bitmap():
    """生成简单的位图作为备选方案"""
    # 随机尺寸：宽度和高度独立变化
    base_width = 1080
    base_height = 1080
    
    # 宽度和高度独立随机变化
    width_variation = random.randint(0, 540)
    height_variation = random.randint(0, 540)
    
    width = base_width + random.choice([-1, 1]) * width_variation
    height = base_height + random.choice([-1, 1]) * height_variation
    
    # 确保在540-1620px范围内
    width = max(540, min(1620, width))
    height = max(540, min(1620, height))
    
    # 创建简单的位图数据
    image_data = bytearray()
    
    # BMP文件头
    file_size = 54 + width * height * 3  # 54字节头 + 像素数据
    image_data.extend(b'BM')  # 签名
    image_data.extend(file_size.to_bytes(4, 'little'))  # 文件大小
    image_data.extend(b'\x00\x00\x00\x00')  # 保留
    image_data.extend((54).to_bytes(4, 'little'))  # 数据偏移
    
    # 信息头
    image_data.extend((40).to_bytes(4, 'little'))  # 信息头大小
    image_data.extend(width.to_bytes(4, 'little'))  # 宽度
    image_data.extend(height.to_bytes(4, 'little'))  # 高度
    image_data.extend((1).to_bytes(2, 'little'))  # 平面数
    image_data.extend((24).to_bytes(2, 'little'))  # 位数
    image_data.extend((0).to_bytes(4, 'little'))  # 压缩
    image_data.extend((width * height * 3).to_bytes(4, 'little'))  # 图像大小
    image_data.extend((2835).to_bytes(4, 'little'))  # X分辨率
    image_data.extend((2835).to_bytes(4, 'little'))  # Y分辨率
    image_data.extend((0).to_bytes(4, 'little'))  # 使用的颜色数
    image_data.extend((0).to_bytes(4, 'little'))  # 重要颜色数
    
    # 生成随机像素数据（从底部开始，因为BMP是自底向上存储）
    for y in range(height):
        for x in range(width):
            # 使用基于位置的伪随机生成相对稳定的图案
            r = (x * 7 + y * 13 + random.randint(0, 100)) % 256
            g = (x * 11 + y * 17 + random.randint(0, 100)) % 256
            b = (x * 5 + y * 19 + random.randint(0, 100)) % 256
            image_data.extend([b, g, r])  # BMP使用BGR顺序
    
    return bytes(image_data)

class ImageServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理所有GET请求，返回程序生成的随机图片"""
        try:
            # 生成随机图片数据
            image_data = generate_random_image()
            
            # 确定MIME类型
            mime_type = "image/png"  # 生成的图片使用PNG格式
            
            # 发送HTTP响应
            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(image_data)))
            self.send_header("Access-Control-Allow-Origin", "*")  # 允许跨域访问
            self.end_headers()
            
            # 发送图片数据
            self.wfile.write(image_data)
            
            # 记录生成的图片信息
            print(f"[{self.date_time_string()}] 生成了新的随机图片 ({len(image_data)} 字节)")

        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

    def do_POST(self):
        """处理所有POST请求，同样返回图片文件"""
        self.do_GET()

    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.date_time_string()}] {format % args}")

    def get_timestamp(self):
        """获取当前时间戳"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def run_server(host="localhost", port=8080, use_https=False):
    """运行图片服务器
    
    Args:
        host: 服务器主机地址
        port: 服务器端口
        use_https: 是否启用HTTPS支持
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, ImageServerHandler)

    if use_https:
        # 创建自签名证书（简化版本，实际使用中可以预生成）
        cert_file = "server.pem"
        if not os.path.exists(cert_file):
            print("正在生成自签名证书...")
            # 生成简单的自签名证书
            try:
                from cryptography import x509
                from cryptography.x509.oid import NameOID
                from cryptography.hazmat.primitives import hashes
                from cryptography.hazmat.primitives.asymmetric import rsa
                from cryptography.hazmat.primitives import serialization
                import datetime

                # 生成私钥
                private_key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=2048,
                )

                # 生成证书
                subject = issuer = x509.Name([
                    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "State"),
                    x509.NameAttribute(NameOID.LOCALITY_NAME, "City"),
                    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ImageServer"),
                    x509.NameAttribute(NameOID.COMMON_NAME, host),
                ])

                cert = x509.CertificateBuilder().subject_name(
                    subject
                ).issuer_name(
                    issuer
                ).public_key(
                    private_key.public_key()
                ).serial_number(
                    x509.random_serial_number()
                ).not_valid_before(
                    datetime.datetime.utcnow()
                ).not_valid_after(
                    datetime.datetime.utcnow() + datetime.timedelta(days=365)
                ).add_extension(
                    x509.SubjectAlternativeName([
                        x509.DNSName(host),
                        x509.DNSName("localhost"),
                        x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                    ]),
                    critical=False,
                ).sign(private_key, hashes.SHA256())

                # 写入证书文件
                with open(cert_file, "wb") as f:
                    f.write(private_key.serialize(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()
                    ))
                    f.write(cert.serialize(encoding=serialization.Encoding.PEM))

                print("自签名证书生成完成")
            except ImportError:
                print("警告: 缺少cryptography库，无法生成自签名证书")
                print("HTTPS功能将被禁用，请安装cryptography库: pip install cryptography")
                use_https = False
            except Exception as e:
                print(f"生成证书失败: {e}")
                use_https = False

        if use_https:
            try:
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                context.load_cert_chain(cert_file)
                httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
                protocol = "https"
            except Exception as e:
                print(f"HTTPS配置失败: {e}")
                print("降级为HTTP模式")
                protocol = "http"
        else:
            protocol = "http"
    else:
        protocol = "http"

    print(f"图片服务器启动成功!")
    print(f"服务器地址: {protocol}://{host}:{port}")
    print(f"每次请求都会生成新的随机程序化图片")
    print(f"图片尺寸: 宽度540-1620px，高度540-1620px (基准1080px ± 0-540px，长宽独立变化)")
    if use_https and protocol == "https":
        print("注意: 使用的是自签名证书，浏览器会显示安全警告")
    print("按 Ctrl+C 停止服务器")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器正在停止...")
        httpd.shutdown()
        print("服务器已停止")


if __name__ == "__main__":
    # 可以修改这里的端口和是否启用HTTPS
    # run_server(port=9180, use_https=True)  # 启用HTTPS支持
    run_server(port=9180, use_https=False)  # 默认使用HTTP
