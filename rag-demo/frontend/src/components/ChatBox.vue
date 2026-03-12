<template>
  <div class="chat-box">
    <input 
      v-model="question" 
      :placeholder="placeholder"
      :disabled="disabled"
      @keyup.enter="send"
    />
    <button @click="send" :disabled="disabled || !question.trim()">
      {{ disabled ? '发送中...' : '发送' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  },
  placeholder: {
    type: String,
    default: '输入你的问题...'
  }
})

const emit = defineEmits(['send'])

const question = ref('')

const send = () => {
  if (question.value.trim() && !props.disabled) {
    emit('send', question.value)
    question.value = ''
  }
}
</script>
