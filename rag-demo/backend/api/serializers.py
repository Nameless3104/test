"""
序列化器 - API 应用

定义 API 接口的输入输出序列化器。
"""
from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    """
    聊天请求序列化器
    
    用于验证用户提交的问题。
    """
    question = serializers.CharField(
        max_length=2000,
        help_text='用户问题，最大2000字符'
    )


class SourceDocumentSerializer(serializers.Serializer):
    """
    来源文档序列化器
    
    用于格式化 RAG 检索到的来源文档。
    """
    content = serializers.CharField(help_text='文档内容片段')
    source = serializers.CharField(help_text='来源文件名')


class ChatResponseSerializer(serializers.Serializer):
    """
    聊天响应序列化器
    
    用于格式化 RAG 系统的回答。
    """
    answer = serializers.CharField(help_text='AI 生成的回答')
    sources = SourceDocumentSerializer(many=True, help_text='来源文档列表')


class DocumentSerializer(serializers.Serializer):
    """
    文档信息序列化器
    
    用于格式化文档列表中的文档信息。
    """
    name = serializers.CharField(help_text='文档名称')
    size = serializers.IntegerField(help_text='文件大小(字节)')


class DocumentListResponseSerializer(serializers.Serializer):
    """
    文档列表响应序列化器
    
    用于格式化文档列表 API 的响应。
    """
    documents = DocumentSerializer(many=True, help_text='文档列表')
