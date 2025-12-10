import os
from typing import Dict, Optional   
import logging

logger = logging.getLogger(__name__)

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..","prompts")

SEARCH_DIR = ["system","tasks","few_shots"]


def load_prompt(name: str) -> Dict[str, str]:
    """
    通过name来load prompt文件
    """

    """
    1. 如果name中包含"/"，则根据"/"来split，第一个部分为group，第二个部分为filename
    2. 如果name中不包含"/"，则默认group为SEARCH_DIR中的所有目录
    """
    
    if "/" in name:
        group, filename = name.split("/",1)
        search_path = group
    else:
        filename = name
        search_path = SEARCH_DIR
    
    # 遍历search_path中的所有目录，查找filename
    file_path = None
    for dir in search_path:
        candidate = os.path.join(BASE_DIR,dir,f"{filename}.md")
        logger.error(f"Searching for prompt file: {candidate}")
        if os.path.exists(candidate):
            file_path = candidate
            break
    if file_path is None:
        raise FileNotFoundError(f"Prompt file {name} not found in {SEARCH_DIR}")

    # 读取文件内容
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    metadata = {}
    content_lines = []

    for line in lines:
        if line.startswith("# "):
            # 解析metadata
            try:
                key, value = line[2:].split(":",1)
                metadata[key.strip()] = value.strip()
            except ValueError:
                # 忽略格式错误的metadata行
                pass
        else:
            content_lines.append(line)

    return {
        "role": metadata.get("role","system"),
        "name": metadata.get("name",filename),
        "description": metadata.get("description",""),
        "content": "".join(content_lines).strip(),
    }
    
