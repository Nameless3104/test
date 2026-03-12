"""
API 应用配置
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """API 应用的配置类"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'API 接口'
