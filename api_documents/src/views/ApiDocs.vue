<template>
  <div class="api-docs">
    <div class="section-intro">
      <h1>🔌 API 接口文档</h1>
      <p>RAG Demo 后端 REST API 接口说明</p>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-post">POST</span>
        <span class="endpoint">/api/chat/</span>
      </div>
      <h3>聊天问答接口</h3>
      <p>基于 RAG 的智能问答接口，返回答案及相关文档来源。</p>
      
      <h4>请求参数</h4>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>参数名</th>
              <th>类型</th>
              <th>必填</th>
              <th>说明</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>question</code></td>
              <td>string</td>
              <td><span class="tag tag-required">必填</span></td>
              <td>用户问题</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h4>请求示例</h4>
      <pre><code>{
  "question": "什么是 RAG？"
}</code></pre>

      <h4>响应参数</h4>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>参数名</th>
              <th>类型</th>
              <th>说明</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>answer</code></td>
              <td>string</td>
              <td>RAG 生成的回答</td>
            </tr>
            <tr>
              <td><code>sources</code></td>
              <td>array</td>
              <td>相关文档来源列表</td>
            </tr>
            <tr>
              <td><code>sources[].content</code></td>
              <td>string</td>
              <td>文档片段内容</td>
            </tr>
            <tr>
              <td><code>sources[].source</code></td>
              <td>string</td>
              <td>文档来源文件名</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h4>响应示例</h4>
      <pre><code>{
  "answer": "RAG (Retrieval-Augmented Generation) 是一种...",
  "sources": [
    {
      "content": "RAG 是检索增强生成技术...",
      "source": "rag_intro.txt"
    }
  ]
}</code></pre>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-get">GET</span>
        <span class="endpoint">/api/documents/</span>
      </div>
      <h3>文档列表接口</h3>
      <p>获取已上传的文档列表。</p>

      <h4>响应参数</h4>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>参数名</th>
              <th>类型</th>
              <th>说明</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>documents</code></td>
              <td>array</td>
              <td>文档列表</td>
            </tr>
            <tr>
              <td><code>documents[].name</code></td>
              <td>string</td>
              <td>文档名称</td>
            </tr>
            <tr>
              <td><code>documents[].size</code></td>
              <td>number</td>
              <td>文档大小（字节）</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-post">POST</span>
        <span class="endpoint">/api/documents/upload/</span>
      </div>
      <h3>文档上传接口</h3>
      <p>上传文档到系统，支持 txt, md, pdf, docx, csv, json 格式。</p>

      <h4>请求参数</h4>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>参数名</th>
              <th>类型</th>
              <th>必填</th>
              <th>说明</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>file</code></td>
              <td>file</td>
              <td><span class="tag tag-required">必填</span></td>
              <td>上传的文件</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="badge badge-post">POST</span>
        <span class="endpoint">/api/vectordb/rebuild/</span>
      </div>
      <h3>重建向量数据库</h3>
      <p>重新构建向量数据库，用于更新文档索引。</p>

      <h4>响应参数</h4>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>参数名</th>
              <th>类型</th>
              <th>说明</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>message</code></td>
              <td>string</td>
              <td>操作结果消息</td>
            </tr>
            <tr>
              <td><code>document_count</code></td>
              <td>number</td>
              <td>处理的文档数量</td>
            </tr>
            <tr>
              <td><code>chunk_count</code></td>
              <td>number</td>
              <td>生成的文档块数量</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.api-docs {
  max-width: 900px;
}

h4 {
  font-size: 16px;
  margin: 20px 0 10px;
  color: #4b5563;
}
</style>
