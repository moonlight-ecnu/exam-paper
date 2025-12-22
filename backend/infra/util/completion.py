import base64
import os

import requests

def parser_base64_img(img_path, prompt="")->str:
    """
    调用模型生成html内容
    :param:
    img_path 图片路径
    prompt 提示词，为空则用默认prompt替换
    :return:
    html内容文本（带```标识，使用时应手动去除）
    """
    # 1. 编码图片
    with open(img_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode('utf-8')

    # 2. 准备请求数据=
    url = "https://chat.ecnu.edu.cn/open/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv("API_KEY")}"
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
    response = requests.post(url, headers=headers, json=data)

    # 4. 处理响应
    if response.status_code == 200:
        result = response.json()
        # TODO 网络不稳定或响应格式不稳定，choices字段可能不存在，需加上可靠的响应处理逻辑
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API请求失败: {response.status_code} - {response.text}")


if __name__ == "__main__":
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phy-07-final-test.jpg")

    # 提示词
    prompt = """请分析这张试卷图片，并生成对应的HTML格式试卷。
        要求：
        1. 仅保留原题干的部分，忽略所有涂改和笔记
        2. 使用合适的HTML标签
        3. 保持试卷的结构和格式，包括出现的图表，请你绘制出这些图表，嵌入html中
        4. 输出完整的HTML文档
        请直接输出HTML代码，不要有其他解释。"""
try:
    html_result = parser_base64_img(image_path, prompt)
    print(html_result)
except Exception as e:
    print(f"错误: {e}")
