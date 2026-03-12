<template>
  <div class="home">
    <header class="header">
      <h1>RAG Demo - AI Knowledge Base</h1>
      <p>基于检索增强生成的智能问答系统</p>
    </header>
    
    <main class="main-content">
      <MessageList :messages="messages" :loading="loading" />
      <ChatBox @send="handleSend" :disabled="loading" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MessageList from '../components/MessageList.vue'
import ChatBox from '../components/ChatBox.vue'
import { sendQuestion } from '../api/chat'

const messages = ref([])
const loading = ref(false)
let messageId = 0

const handleSend = async (question) => {
  if (!question.trim()) return
  
  // Add user message
  messages.value.push({
    id: ++messageId,
    role: 'user',
    content: question
  })
  
  loading.value = true
  
  // Add loading message
  const loadingId = ++messageId
  messages.value.push({
    id: loadingId,
    role: 'assistant',
    content: '',
    loading: true
  })
  
  try {
    const response = await sendQuestion(question)
    
    // Remove loading message and add response
    messages.value = messages.value.filter(m => m.id !== loadingId)
    
    messages.value.push({
      id: ++messageId,
      role: 'assistant',
      content: response.answer || response.response || '收到回复',
      sources: response.sources || null
    })
  } catch (error) {
    // Remove loading message and add error
    messages.value = messages.value.filter(m => m.id !== loadingId)
    
    messages.value.push({
      id: ++messageId,
      role: 'assistant',
      content: `错误: ${error.message}`,
      error: true
    })
  } finally {
    loading.value = false
  }
}
</script>
