<template>
  <div :class="['message', message.role, { loading: message.loading, error: message.error }]">
    <div class="content">
      <template v-if="message.loading">
        <div class="loading-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <span>思考中...</span>
      </template>
      <template v-else>
        {{ message.content }}
      </template>
    </div>
    <SourceCard v-if="message.sources && message.sources.length" :sources="message.sources" />
  </div>
</template>

<script setup>
import SourceCard from './SourceCard.vue'

defineProps({
  message: {
    type: Object,
    required: true
  }
})
</script>
