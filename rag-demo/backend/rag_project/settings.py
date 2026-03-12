"""
Django 设置文件 - RAG 项目后端配置

包含 Django 项目的所有配置项，包括：
- 数据库配置
- 已安装的应用
- 中间件
- REST Framework 配置
- CORS 配置
"""

import os
from pathlib import Path

# 加载 .env 文件
from dotenv import load_dotenv
env_file = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_file)

# 项目基础目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全密钥 - 生产环境请修改！
SECRET_KEY = 'django-insecure-rag-demo-key-please-change-in-production'

# 调试模式 - 生产环境设为 False
DEBUG = True

# 允许访问的主机
ALLOWED_HOSTS = ['*']

# 已安装的应用
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 第三方应用
    'rest_framework',
    'corsheaders',
    
    # 本地应用
    'api',
    'rag',
]

# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS 中间件，需放在 CommonMiddleware 之前
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 根 URL 配置
ROOT_URLCONF = 'rag_project.urls'

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 应用
WSGI_APPLICATION = 'rag_project.wsgi.application'

# 数据库配置 - 使用 SQLite (开发环境)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 密码验证器
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 国际化配置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# 静态文件配置
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 媒体文件配置
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 默认主键类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============ Django REST Framework 配置 ============
REST_FRAMEWORK = {
    # 默认渲染器
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # 默认解析器
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

# ============ CORS 配置 ============
# 允许所有域名访问 (开发环境)
CORS_ALLOW_ALL_ORIGINS = True

# 允许的请求方法
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# 允许的请求头
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ============ RAG 项目配置 ============
# 数据目录
RAG_DATA_DIR = BASE_DIR / 'data'

# 向量数据库目录
RAG_VECTORDB_DIR = BASE_DIR / 'vectordb'

# DeepSeek API 配置 (优先)
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
DEEPSEEK_BASE_URL = os.environ.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')

# OpenAI API 配置 (备用)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL', '')

# LLM 模型配置
LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME', 'deepseek-chat')

# Embedding 模型配置 (使用 text-embedding-3-small 更好的效果)
EMBEDDING_MODEL_NAME = os.environ.get('EMBEDDING_MODEL_NAME', 'text-embedding-3-small')

# 向量数据库配置
VECTORDB_DIR = os.environ.get('VECTORDB_DIR', str(BASE_DIR / 'vectordb_v3'))
