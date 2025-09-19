# 随机图片服务器

这是一个简单的HTTP/HTTPS图片服务器，每次请求都会生成独特的程序化图片，非常适合测试和开发使用。

## 功能特点

- **随机图片生成**: 每次请求都会生成不同的程序化图片
- **尺寸变化**: 图片尺寸在540-1620px范围内随机变化（基准1080px ± 0-540px）
- **程序化纹理**: 包含随机颜色、形状和图案
- **时间戳**: 每张图片都包含生成时间戳和随机种子，确保相对唯一性
- **格式支持**: 支持PIL库时生成PNG格式，否则生成BMP格式
- **HTTP/HTTPS**: 支持HTTP和HTTPS协议（HTTPS需要自签名证书）

## 安装依赖

```bash
pip install -r requirements.txt
```

依赖包括：
- Pillow (PIL): 用于生成丰富的程序化图片
- cryptography: 用于HTTPS自签名证书生成

## 使用方法

### 基本使用（HTTP）

```bash
python server.py
```

服务器将在 `http://localhost:9180` 启动

### 启用HTTPS

```bash
# 修改server.py最后一行
run_server(port=9180, use_https=True)
```

### 自定义配置

```python
# 修改server.py中的参数
run_server(
    host="localhost",    # 主机地址
    port=9180,           # 端口号
    use_https=False      # 是否启用HTTPS
)
```

## 测试验证

### 浏览器访问

打开浏览器访问 `http://localhost:9180`，每次刷新都会看到不同的图片。

### 命令行测试

```bash
# 获取图片信息
curl -I http://localhost:9180/

# 下载图片
curl -o test.png http://localhost:9180/
```

### Python测试

```python
import requests

# 获取随机图片
response = requests.get("http://localhost:9180/")
with open("random_image.png", "wb") as f:
    f.write(response.content)

print(f"图片大小: {len(response.content)} 字节")
print(f"Content-Type: {response.headers.get('content-type')}")
```

## 图片生成特性

- **随机性**: 每次请求生成完全不同的图片
- **尺寸变化**: 宽度和高度独立随机变化，基准1080px ± 0-540px (540-1620px范围)
- **长宽比自由**: 不强制1:1比例，支持横向、纵向、方形各种比例
- **程序化纹理**: 使用PIL库生成丰富的视觉效果
- **时间戳标识**: 图片包含生成时间信息
- **双格式支持**: 同时支持PNG和JPG格式

## 注意事项

- 如果没有安装Pillow库，服务器会自动降级生成简单的BMP位图
- HTTPS使用自签名证书，浏览器会显示安全警告
- 图片完全在内存中生成，不会保存到磁盘
- 所有请求都返回PNG格式图片（除非降级到BMP）

## 用途

- API测试和开发
- 前端UI测试
- 缓存验证
- 负载测试
- 图片处理功能测试

这个服务器特别适合需要验证是否获取到不同图片的测试场景！