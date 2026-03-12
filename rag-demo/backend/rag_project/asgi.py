"""
ASGI 配置文件 - RAG 项目

用于异步部署的 ASGI 入口点。
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rag_project.settings')

application = get_asgi_application()
