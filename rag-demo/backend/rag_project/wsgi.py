"""
WSGI 配置文件 - RAG 项目

用于生产环境部署的 WSGI 入口点。
"""

import os
from pathlib import Path

# 加载 .env 文件
env_file = Path(__file__).resolve().parent.parent / '.env'
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rag_project.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
