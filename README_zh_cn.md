# Curl 命令转换器

这是一个将 curl 命令转换为 Python 请求元素的工具，提供了图形界面，方便用户使用。

## 功能特点

- 解析 curl 命令，提取 URL、请求头、cookie 和 URL 参数等信息
- 支持多行 curl 命令格式
- 支持从剪贴板粘贴和复制到剪贴板
- 支持保存转换结果到文件
- 提供简洁易用的图形界面

## 安装

1. 克隆或下载此仓库
2. 安装依赖包：

```bash
pip install pyperclip==1.8.2
```

## 使用方法

运行主应用程序：

```bash
python curl_converter_app.py
```

### 使用步骤

1. 将 curl 命令粘贴到输入框中（支持直接粘贴从浏览器开发者工具复制的 curl 命令）
2. 点击"转换"按钮
3. 在输出框中查看转换后的 Python 请求元素
4. 可以复制结果或保存到文件

## 示例

### 输入（curl 命令）

```bash
curl 'https://example.com/api/data' \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -b 'session=abc123; user=user1'
```

### 输出（Python 请求元素）

```python
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

cookies = {
    "session": "abc123",
    "user": "user1"
}

url = "https://example.com/api/data"

method = "GET"
```

## 支持的 curl 选项

- URL 提取
- Headers (`-H` 或 `--header`)
- Cookies (`-b` 或 `--cookie`)
- 请求方法 (`-X` 或 `--request`)
- 数据 (`-d` 或 `--data`)
- URL 参数解析

## 开发者

如果您想扩展此工具的功能，可以修改 `curl_parser.py` 文件以支持更多的 curl 选项。 