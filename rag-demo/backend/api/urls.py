"""
URL 路由 - API 应用

定义 API 接口的 URL 路由。
"""
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # 聊天接口 - POST /api/chat/
    path('chat/', views.ChatView.as_view(), name='chat'),
    
    # 文档列表接口 - GET /api/documents/
    path('documents/', views.DocumentListView.as_view(), name='documents'),
    
    # 文档上传接口 - POST /api/documents/upload/
    path('documents/upload/', views.DocumentUploadView.as_view(), name='document-upload'),
    
    # 向量库重建接口 - POST /api/vectordb/rebuild/
    path('vectordb/rebuild/', views.RebuildVectorDBView.as_view(), name='rebuild-vectordb'),
]
