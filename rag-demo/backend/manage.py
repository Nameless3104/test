#!/usr/bin/env python
"""Django 的命令行工具，用于管理项目。"""
import os
import sys
from pathlib import Path


def main():
    """运行管理任务。"""
    # 加载 .env 文件
    env_file = Path(__file__).resolve().parent / '.env'
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rag_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "无法导入 Django。请确保已安装 Django 并且 "
            "虚拟环境已激活。"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
