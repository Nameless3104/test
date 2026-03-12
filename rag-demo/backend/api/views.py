"""
视图函数 - API 应用

实现 RAG 系统的核心 API 接口。
"""
import os
from pathlib import Path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import JsonResponse

from .serializers import (
    ChatRequestSerializer,
    ChatResponseSerializer,
    DocumentSerializer,
    DocumentListResponseSerializer,
)
from rag.loaders import load_documents, split_documents
from rag.embeddings import get_embeddings
from rag.retriever import create_vectorstore, get_retriever, load_vectorstore, hybrid_search
from rag.chain import create_rag_chain, ask_question


class ChatView(APIView):
    """
    聊天接口视图
    
    POST /api/chat/
    请求体: {"question": "用户问题"}
    响应: {"answer": "RAG回答", "sources": [{"content": "来源内容", "source": "文件名"}]}
    """
    
    def post(self, request):
        """
        处理聊天请求
        
        Args:
            request: HTTP 请求对象
            
        Returns:
            Response: 包含回答和来源的响应
        """
        # 验证请求数据
        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': '请求数据无效', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        question = serializer.validated_data['question']
        
        try:
            # 加载或创建向量数据库
            vectordb_path = settings.RAG_VECTORDB_DIR
            embeddings = get_embeddings()
            
            # 尝试加载已有的向量数据库
            try:
                vectorstore = load_vectorstore(vectordb_path, embeddings)
            except Exception:
                # 如果加载失败，尝试从文档创建
                data_dir = settings.RAG_DATA_DIR
                if not data_dir.exists() or not list(data_dir.glob('*')):
                    return Response(
                        {'error': '向量数据库不存在且没有可用文档，请先上传文档'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                documents = load_documents(str(data_dir))
                if not documents:
                    return Response(
                        {'error': '没有找到可用的文档'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                split_docs = split_documents(documents)
                vectorstore = create_vectorstore(split_docs, embeddings, str(vectordb_path))
            
            # 创建检索器
            retriever = get_retriever(vectorstore)
            
            # 使用混合检索获取相关文档（优化后 Recall@3=60%）
            docs = hybrid_search(vectorstore, question, k=4)
            
            # 创建 RAG 链
            rag_chain = create_rag_chain(retriever)
            
            # 执行问答
            result = ask_question(rag_chain, question, retriever)
            
            # 使用混合检索的结果作为来源
            sources = []
            for doc in docs:
                source_path = doc.metadata.get("source", "Unknown")
                content = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                sources.append({
                    "content": content,
                    "source": source_path
                })
            
            # 格式化响应
            response_data = {
                'answer': result.get('answer', ''),
                'sources': sources
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'处理请求时发生错误: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DocumentListView(APIView):
    """
    文档列表接口视图
    
    GET /api/documents/
    响应: {"documents": [{"name": "文档名", "size": 大小}]}
    """
    
    def get(self, request):
        """
        获取文档列表
        
        Args:
            request: HTTP 请求对象
            
        Returns:
            Response: 包含文档列表的响应
        """
        try:
            data_dir = settings.RAG_DATA_DIR
            
            # 确保目录存在
            if not data_dir.exists():
                data_dir.mkdir(parents=True, exist_ok=True)
            
            # 获取所有文档文件
            documents = []
            supported_extensions = ['.txt', '.md', '.pdf', '.docx', '.csv', '.json']
            
            for file_path in data_dir.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                    documents.append({
                        'name': file_path.name,
                        'size': file_path.stat().st_size
                    })
            
            # 按名称排序
            documents.sort(key=lambda x: x['name'])
            
            return Response({'documents': documents}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'获取文档列表时发生错误: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DocumentUploadView(APIView):
    """
    文档上传接口视图
    
    POST /api/documents/upload/
    请求体: multipart/form-data with file
    响应: {"message": "上传成功", "filename": "文件名"}
    """
    
    def post(self, request):
        """
        上传文档
        
        Args:
            request: HTTP 请求对象
            
        Returns:
            Response: 上传结果
        """
        try:
            if 'file' not in request.FILES:
                return Response(
                    {'error': '没有上传文件'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            uploaded_file = request.FILES['file']
            
            # 验证文件类型
            supported_extensions = ['.txt', '.md', '.pdf', '.docx', '.csv', '.json']
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            if file_ext not in supported_extensions:
                return Response(
                    {'error': f'不支持的文件类型: {file_ext}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 确保数据目录存在
            data_dir = settings.RAG_DATA_DIR
            if not data_dir.exists():
                data_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存文件
            file_path = data_dir / uploaded_file.name
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            return Response({
                'message': '上传成功',
                'filename': uploaded_file.name,
                'size': uploaded_file.size
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'上传文件时发生错误: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RebuildVectorDBView(APIView):
    """
    重建向量数据库接口视图
    
    POST /api/vectordb/rebuild/
    响应: {"message": "重建成功", "document_count": 文档数量}
    """
    
    def post(self, request):
        """
        重建向量数据库
        
        Args:
            request: HTTP 请求对象
            
        Returns:
            Response: 重建结果
        """
        try:
            data_dir = settings.RAG_DATA_DIR
            vectordb_path = settings.RAG_VECTORDB_DIR
            
            # 检查数据目录
            if not data_dir.exists() or not list(data_dir.glob('*')):
                return Response(
                    {'error': '数据目录为空，无法重建向量数据库'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 加载文档
            documents = load_documents(str(data_dir))
            if not documents:
                return Response(
                    {'error': '没有找到可用的文档'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # 分块文档
            split_docs = split_documents(documents)
            
            # 获取 embeddings
            embeddings = get_embeddings()
            
            # 创建新的向量数据库
            vectorstore = create_vectorstore(split_docs, embeddings, str(vectordb_path))
            
            return Response({
                'message': '向量数据库重建成功',
                'document_count': len(documents),
                'chunk_count': len(split_docs)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'重建向量数据库时发生错误: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
