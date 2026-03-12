<template>
  <div class="component-docs">
    <div class="section-intro">
      <h1>🧩 前端组件文档</h1>
      <p>RAG Demo 前端 Vue 3 组件说明</p>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="endpoint">ChatPanel.vue</span>
      </div>
      <h3>聊天面板组件</h3>
      <p>核心聊天交互组件，处理用户问答。</p>

      <h4>功能</h4>
      <ul>
        <li>显示聊天历史记录</li>
        <li>用户输入问题</li>
        <li>显示 AI 回答和来源文档</li>
        <li>自动滚动到最新消息</li>
      </ul>

      <h4>依赖</h4>
      <pre><code>import { sendQuestion } from '@/api/chat'</code></pre>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="endpoint">DocumentList.vue</span>
      </div>
      <h3>文档列表组件</h3>
      <p>显示已上传的文档列表。</p>

      <h4>功能</h4>
      <ul>
        <li>显示文档名称和大小</li>
        <li>刷新文档列表</li>
        <li>上传新文档</li>
      </ul>

      <h4>依赖</h4>
      <pre><code>import { getDocuments } from '@/api/chat'</code></pre>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="endpoint">api/chat.js</span>
      </div>
      <h3>API 调用模块</h3>
      <p>封装后端 API 调用。</p>

      <h4>导出函数</h4>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>函数名</th>
              <th>参数</th>
              <th>返回值</th>
              <th>说明</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>sendQuestion</code></td>
              <td>question: string</td>
              <td>Promise&lt;object&gt;</td>
              <td>发送问题到后端</td>
            </tr>
            <tr>
              <td><code>getDocuments</code></td>
              <td>无</td>
              <td>Promise&lt;object&gt;</td>
              <td>获取文档列表</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h4>代码示例</h4>
      <pre><code>// 发送问题
const result = await sendQuestion("什么是 RAG？");
console.log(result.answer);

// 获取文档列表
const docs = await getDocuments();
console.log(docs.documents);</code></pre>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.component-docs {
  max-width: 900px;
}

h4 {
  font-size: 16px;
  margin: 20px 0 10px;
  color: #4b5563;
}

ul {
  margin: 10px 0;
  padding-left: 20px;
}

li {
  margin: 8px 0;
  color: #4b5563;
}
</style>
