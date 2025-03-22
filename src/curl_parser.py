import json
import re
import urllib.parse
from typing import Dict, Any


def parse_curl_command(curl_command: str) -> Dict[str, Any]:
    """
    解析curl命令，提取URL、请求头、cookie和URL参数
    
    Args:
        curl_command: curl命令字符串
        
    Returns:
        包含解析结果的字典，包括url、headers、cookies、params等
    """
    # 处理多行命令（将反斜杠连接的多行合并为单行）
    curl_command = re.sub(r'\\\s*\n\s*', ' ', curl_command)
    
    # 提取URL
    url_match = re.search(r'curl\s+["\']?([^"\']+)["\']?', curl_command)
    if not url_match:
        url_match = re.search(r'curl\s+(-[A-Za-z]+\s+[\'"][^\'"]+"[\'"])?\s*([^\s\'"]+)', curl_command)
    
    if not url_match:
        raise ValueError("cannot find URL")
    
    full_url = url_match.group(1) if url_match.group(1) else url_match.group(2)
    
    # 去除引号
    full_url = full_url.strip("'\"")
    
    # 解析URL和查询参数
    parsed_url = urllib.parse.urlparse(full_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    query_params = dict(urllib.parse.parse_qsl(parsed_url.query))
    
    # 提取请求头
    headers = {}
    header_matches = re.finditer(r'-H\s*["\']([^:]+):\s*([^\']*)["\']', curl_command)
    for match in header_matches:
        header_name = match.group(1).strip()
        header_value = match.group(2).strip()
        headers[header_name] = header_value
    
    # 提取cookies
    cookies = {}
    cookie_matches = re.finditer(r'-b\s*["\']([^\']*)["\']', curl_command)
    for match in cookie_matches:
        cookie_str = match.group(1).strip()
        if cookie_str:
            # 处理多个cookie
            pairs = cookie_str.split(';')
            for pair in pairs:
                if '=' in pair:
                    name, value = pair.strip().split('=', 1)
                    cookies[name] = value
    
    # 检查是否有data或json参数
    data = None
    data_match = re.search(r'--data-raw\s*["\']([^\']*)["\']', curl_command)
    if data_match:
        data_str = data_match.group(1)
        try:
            # 尝试解析为JSON
            data = json.loads(data_str)
        except json.JSONDecodeError:
            # 如果不是JSON，则解析为表单数据
            data = dict(urllib.parse.parse_qsl(data_str))
    
    # 检查请求方法
    method = "GET"  # 默认为GET
    if "-X" in curl_command or "--request" in curl_command:
        method_match = re.search(r'-X\s+(\S+)', curl_command)
        if not method_match:
            method_match = re.search(r'--request\s+(\S+)', curl_command)
        if method_match:
            method = method_match.group(1).upper()
    elif data is not None or "-d" in curl_command or "--data" in curl_command:
        method = "POST"  # 如果有数据但没指定方法，假设为POST
    
    return {
        "url": base_url,
        "params": query_params,
        "headers": headers,
        "cookies": cookies,
        "data": data,
        "method": method
    }


def format_dict(d: Dict, indent: int = 4) -> str:
    """
    将字典格式化为美观的字符串表示
    
    Args:
        d: 要格式化的字典
        indent: 缩进空格数
        
    Returns:
        格式化后的字符串
    """
    if not d:
        return "{}"
    
    lines = ["{\n"]
    for key, value in d.items():
        # 处理值中的引号
        if isinstance(value, str):
            if '\"' in value:
                value = f'\"{value.replace('\"', '\\\"')}\"'
            else:
                value = f'\"{value}\"'
        lines.append(f"{' ' * indent}\"{key}\": {value},\n")
    
    # 删除最后一个逗号
    if len(lines) > 1:
        lines[-1] = lines[-1][:-2] + "\n"
    
    lines.append("}")
    return "".join(lines)


def curl_to_python(curl_command: str) -> str:
    """
    将curl命令转换为Python请求元素的文本表示
    
    Args:
        curl_command: curl命令字符串
        
    Returns:
        包含Python请求元素的文本
    """
    try:
        parsed = parse_curl_command(curl_command)
        
        result = []
        
        # 格式化headers
        if parsed["headers"]:
            result.append(f"headers = {format_dict(parsed['headers'])}")
        
        # 格式化cookies
        if parsed["cookies"]:
            result.append(f"cookies = {format_dict(parsed['cookies'])}")
        
        # 添加URL
        result.append(f"url = \"{parsed['url']}\"")
        
        # 格式化params
        if parsed["params"]:
            result.append(f"params = {format_dict(parsed['params'])}")
        
        # 格式化data
        if parsed["data"]:
            if isinstance(parsed["data"], dict):
                result.append(f"data = {format_dict(parsed['data'])}")
            else:
                result.append(f"data = {json.dumps(parsed['data'], indent=4)}")
        
        # 添加请求方法
        result.append(f"method = \"{parsed['method']}\"")
        
        return "\n\n".join(result)
    except Exception as e:
        return f"parse error: {str(e)}"
