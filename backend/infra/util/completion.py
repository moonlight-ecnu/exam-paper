import base64
import os
import requests
from backend.infra.config.config import conf

def parser_img_bytes(img_bytes: bytes, prompt="") -> str:
    """
    调用模型生成html内容
    :param img_bytes: 图片字节流
    :param prompt: 提示词
    :return: html内容文本
    """
    # 1. 编码图片
    base64_image = base64.b64encode(img_bytes).decode('utf-8')

    # 2. 准备请求数据
    base_url = conf.get("BASE_URL", "https://chat.ecnu.edu.cn/open/api/v1/chat/completions")
    api_key = conf.get("API_KEY", os.getenv("API_KEY"))

    if not api_key:
        raise Exception("API Key not configured")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "ecnu-vl",
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt if prompt != "" else """请分析这张试卷图片，并生成对应的HTML格式试卷。
        要求：
        1. 仅保留原题干的部分，忽略所有涂改和笔记
        2. 使用合适的HTML标签
        3. 保持试卷的结构和格式，包括大小题号、出现的图表等，如有图表，请遵照图标原样绘制并嵌入html中
        4. 输出完整的HTML文档
        请直接输出HTML代码，不要有其他解释。"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    }

    # 3. 发送请求
    try:
        response = requests.post(base_url, headers=headers, json=data, timeout=60)
    except requests.exceptions.RequestException as e:
        raise Exception(f"API Request Failed: {e}")

    # 4. 处理响应
    if response.status_code == 200:
        result = response.json()
        try:
            return result["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
             raise Exception(f"API Response format error: {result}")
    else:
        raise Exception(f"API请求失败: {response.status_code} - {response.text}")

def parser_base64_img(img_path, prompt="") -> str:
    """
    Wrapper for file path input
    """
    with open(img_path, "rb") as f:
        return parser_img_bytes(f.read(), prompt)

if __name__ == "__main__":
    pass
