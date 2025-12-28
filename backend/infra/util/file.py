def save_to_file(filename: str, content: str):
    """
    保存文本内容为文件
    """
    with open(filename, 'w') as f:
        f.write(content)
