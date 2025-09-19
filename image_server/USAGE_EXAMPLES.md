# 图片服务器使用示例

## 快速开始

### 1. 启动服务器

```bash
# 方法1：直接运行Python脚本
python server.py

# 方法2：使用启动脚本（Windows）
start.bat

# 方法3：使用启动脚本（Python）
python start_server.py
```

### 2. 访问图片

服务器启动后，可以通过浏览器或任何HTTP客户端访问：

```
http://localhost:9180
```

### 3. 测试服务器

运行测试脚本验证服务器是否正常工作：

```bash
python simple_test.py
```

## 使用场景示例

### 在HTML中使用

```html
<!DOCTYPE html>
<html>
<head>
    <title>图片服务器测试</title>
</head>
<body>
    <h1>图片服务器测试</h1>
    <img src="http://localhost:9180/any-image.jpg" alt="测试图片">
    <img src="http://localhost:9180/test.png" alt="测试图片2">
</body>
</html>
```

### 在Python中使用

```python
import urllib.request

# 获取图片
default_image_url = "http://localhost:9180/default.jpg"
response = urllib.request.urlopen(default_image_url)
image_data = response.read()

# 保存图片
with open("downloaded_image.jpg", "wb") as f:
    f.write(image_data)
```

### 在命令行中使用curl

```bash
# 获取图片并保存到文件
curl -o image.jpg http://localhost:9180/

# 获取图片信息（HEAD请求）
curl -I http://localhost:9180/test.jpg
```

## 高级配置

### 修改端口

在 `server.py` 中修改：
```python
def run_server(host='localhost', port=9180):
```

### 修改图片文件

在 `server.py` 中修改：
```python
image_path = r"C:\Users\wumingjie\Pictures\Default.jpg"
```

### 允许外部访问

在 `start_server.py` 中修改：
```python
HOST = '0.0.0.0'  # 允许任何IP访问
```

## 注意事项

1. **防火墙设置**：如果要从其他设备访问，需要确保防火墙允许相应的端口
2. **图片文件**：确保指定的图片文件存在且可读
3. **端口冲突**：如果端口被占用，可以修改为其他端口（如8081、8082等）
4. **性能考虑**：这个服务器是单线程的，适合测试和开发使用

## 故障排除

### 端口被占用

如果看到类似错误：
```
OSError: [Errno 48] Address already in use
```

解决方法：
1. 修改端口号
2. 找到并停止占用该端口的程序

### 图片文件不存在

如果看到类似错误：
```
Image file not found
```

解决方法：
1. 检查图片文件路径是否正确
2. 确保文件存在且可读
3. 检查文件权限

### 权限问题

如果遇到权限错误，请确保：
1. Python有权限读取图片文件
2. 有权限绑定到指定端口（某些系统需要管理员权限）