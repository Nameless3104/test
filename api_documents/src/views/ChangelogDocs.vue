<template>
  <div class="changelog-docs">
    <div class="section-intro">
      <h1>📝 改动记录</h1>
      <p>2026-03-11 项目改动记录</p>
    </div>

    <div class="card">
      <h3>🚀 召回率优化</h3>
      <p class="date">2026-03-11 下午</p>
      
      <div class="change-item">
        <h4>混合检索实现</h4>
        <p>新增 <code>hybrid_search()</code> 函数，结合相似度检索和 MMR 检索。</p>
        <div class="stats">
          <span class="stat-badge success">Recall@3: 42% → 60%</span>
        </div>
      </div>

      <div class="change-item">
        <h4>Embedding 模型升级</h4>
        <p>从 text-embedding-ada-002 升级到 text-embedding-3-small。</p>
        <div class="stats">
          <span class="stat-badge success">Recall@3: 60% → 66%</span>
          <span class="stat-badge success">MRR: 0.39 → 0.45</span>
        </div>
      </div>
    </div>

    <div class="card">
      <h3>🔧 DeepSeek API 适配</h3>
      <p class="date">2026-03-11 下午</p>
      
      <div class="change-item">
        <h4>LLM 切换到 DeepSeek</h4>
        <ul>
          <li>更新 <code>.env</code> 配置</li>
          <li>更新 <code>settings.py</code> 添加 DEEPSEEK_API_KEY</li>
          <li>更新 <code>chain.py</code> 支持 DeepSeek API</li>
        </ul>
      </div>

      <div class="change-item">
        <h4>Embedding 保持 OpenAI</h4>
        <p>DeepSeek 不提供 embedding API，继续使用 OpenAI text-embedding-3-small。</p>
      </div>
    </div>

    <div class="card">
      <h3>📊 CRAG 数据集集成</h3>
      <p class="date">2026-03-11 上午</p>
      
      <div class="change-item">
        <h4>数据处理</h4>
        <ul>
          <li>处理 CRAG Task 1 & 2 数据集</li>
          <li>生成 100 个文档，50 个测试问题</li>
          <li>创建向量数据库</li>
        </ul>
      </div>

      <div class="change-item">
        <h4>召回率测试</h4>
        <p>创建测试脚本 <code>test_recall.py</code>，测试不同配置的召回率。</p>
      </div>
    </div>

    <div class="card">
      <h3>📁 文件变更列表</h3>
      
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>文件路径</th>
              <th>变更类型</th>
              <th>说明</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>backend/rag/retriever.py</code></td>
              <td><span class="badge badge-modified">修改</span></td>
              <td>新增 hybrid_search() 函数</td>
            </tr>
            <tr>
              <td><code>backend/rag/chain.py</code></td>
              <td><span class="badge badge-modified">修改</span></td>
              <td>支持 DeepSeek API</td>
            </tr>
            <tr>
              <td><code>backend/rag/embeddings.py</code></td>
              <td><span class="badge badge-modified">修改</span></td>
              <td>支持 text-embedding-3-small</td>
            </tr>
            <tr>
              <td><code>backend/api/views.py</code></td>
              <td><span class="badge badge-modified">修改</span></td>
              <td>ChatView 使用混合检索</td>
            </tr>
            <tr>
              <td><code>backend/.env</code></td>
              <td><span class="badge badge-modified">修改</span></td>
              <td>添加 DeepSeek API 配置</td>
            </tr>
            <tr>
              <td><code>backend/vectordb_v3/</code></td>
              <td><span class="badge badge-new">新增</span></td>
              <td>新向量数据库 (text-embedding-3-small)</td>
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
.changelog-docs {
  max-width: 900px;
}

.date {
  color: #6b7280;
  font-size: 14px;
  margin-bottom: 15px;
}

.change-item {
  margin: 20px 0;
  padding: 15px;
  background: #f9fafb;
  border-radius: 8px;
}

.change-item h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #374151;
}

.change-item p {
  margin: 0;
}

.change-item ul {
  margin: 10px 0 0 0;
  padding-left: 20px;
}

.change-item li {
  margin: 5px 0;
  color: #4b5563;
}

.stats {
  margin-top: 10px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.stat-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.stat-badge.success {
  background: #dcfce7;
  color: #15803d;
}

.badge-modified {
  background: #fef3c7;
  color: #b45309;
}

.badge-new {
  background: #dcfce7;
  color: #15803d;
}
</style>
