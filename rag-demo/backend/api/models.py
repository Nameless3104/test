"""
数据模型 - API 应用

定义文档相关的数据模型。
"""
from django.db import models


class Document(models.Model):
    """
    文档模型
    
    存储上传文档的元数据信息。
    """
    name = models.CharField('文档名称', max_length=255)
    file_path = models.CharField('文件路径', max_length=500)
    file_size = models.IntegerField('文件大小(字节)', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '文档'
        verbose_name_plural = '文档列表'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class ChatHistory(models.Model):
    """
    聊天历史模型
    
    记录用户的问答历史。
    """
    question = models.TextField('用户问题')
    answer = models.TextField('AI回答')
    sources = models.JSONField('来源文档', default=list, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '聊天记录'
        verbose_name_plural = '聊天历史'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Q: {self.question[:50]}..."
