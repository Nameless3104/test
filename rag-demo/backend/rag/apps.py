"""
RAG 应用配置
"""
from django.apps import AppConfig


class RagConfig(AppConfig):
    """RAG 应用的配置类"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rag'
    verbose_name = 'RAG 模块'
