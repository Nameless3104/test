<template>
  <div class="app">
    <nav class="sidebar">
      <div class="logo">
        <span class="logo-icon">📚</span>
        <span class="logo-text">RAG Demo Docs</span>
      </div>
      <ul class="nav-menu">
        <li 
          v-for="item in navItems" 
          :key="item.id"
          :class="['nav-item', { active: activeSection === item.id }]"
          @click="activeSection = item.id"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span>{{ item.title }}</span>
        </li>
      </ul>
      <div class="nav-footer">
        <p>生成日期: 2026-03-11</p>
      </div>
    </nav>
    
    <main class="content">
      <ApiDocs v-if="activeSection === 'api'" />
      <ComponentDocs v-else-if="activeSection === 'components'" />
      <ChangelogDocs v-else-if="activeSection === 'changelog'" />
      <OverviewDocs v-else />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ApiDocs from './views/ApiDocs.vue'
import ComponentDocs from './views/ComponentDocs.vue'
import ChangelogDocs from './views/ChangelogDocs.vue'
import OverviewDocs from './views/OverviewDocs.vue'

const activeSection = ref('overview')

const navItems = [
  { id: 'overview', title: '概述', icon: '🏠' },
  { id: 'api', title: 'API 接口', icon: '🔌' },
  { id: 'components', title: '前端组件', icon: '🧩' },
  { id: 'changelog', title: '改动记录', icon: '📝' }
]
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: #f5f7fa;
  color: #333;
  line-height: 1.6;
}

.app {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 260px;
  background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
  color: #fff;
  padding: 20px 0;
  position: fixed;
  height: 100vh;
  overflow-y: auto;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 20px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  margin-bottom: 20px;
}

.logo-icon {
  font-size: 28px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
}

.nav-menu {
  list-style: none;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: rgba(255,255,255,0.1);
}

.nav-item.active {
  background: rgba(99, 102, 241, 0.3);
  border-left-color: #6366f1;
}

.nav-icon {
  font-size: 18px;
}

.nav-footer {
  position: absolute;
  bottom: 20px;
  left: 20px;
  right: 20px;
  font-size: 12px;
  color: rgba(255,255,255,0.5);
}

.content {
  flex: 1;
  margin-left: 260px;
  padding: 40px;
  max-width: 1200px;
}

h1 {
  font-size: 32px;
  margin-bottom: 20px;
  color: #1a1a2e;
}

h2 {
  font-size: 24px;
  margin: 30px 0 15px;
  color: #16213e;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 10px;
}

h3 {
  font-size: 18px;
  margin: 20px 0 10px;
  color: #374151;
}

p {
  margin-bottom: 15px;
  color: #4b5563;
}

code {
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 14px;
  color: #6366f1;
}

pre {
  background: #1a1a2e;
  color: #e5e7eb;
  padding: 20px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 15px 0;
}

pre code {
  background: none;
  padding: 0;
  color: inherit;
}

.table-container {
  overflow-x: auto;
  margin: 15px 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

th, td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

th {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
}

tr:hover {
  background: #f9fafb;
}

.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.badge-get {
  background: #dbeafe;
  color: #1d4ed8;
}

.badge-post {
  background: #dcfce7;
  color: #15803d;
}

.badge-put {
  background: #fef3c7;
  color: #b45309;
}

.badge-delete {
  background: #fee2e2;
  color: #b91c1c;
}

.card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  margin: 20px 0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.endpoint {
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 14px;
  color: #6366f1;
}

.section-intro {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 30px;
  border-radius: 12px;
  margin-bottom: 30px;
}

.section-intro h1 {
  color: #fff;
  margin-bottom: 10px;
}

.section-intro p {
  color: rgba(255,255,255,0.9);
}

.tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-right: 6px;
}

.tag-required {
  background: #fee2e2;
  color: #b91c1c;
}

.tag-optional {
  background: #e0e7ff;
  color: #3730a3;
}
</style>
