<template>
  <div class="message-list">
    <div v-if="messages.length === 0" class="message-list-empty">
      <div class="icon">💬</div>
      <p>开始对话吧！输入你的问题...</p>
    </div>
    <MessageItem 
      v-for="msg in messages" 
      :key="msg.id" 
      :message="msg"
    />
  </div>
</template>

<script setup>
import MessageItem from './MessageItem.vue'

defineProps({
  messages: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})
</script>
