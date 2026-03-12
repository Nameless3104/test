<template>
  <div class="sources">
    <div class="sources-title">📎 参考来源</div>
    <div class="source" v-for="(src, i) in sources" :key="i">
      {{ src.source || src.title || src }}
    </div>
  </div>
</template>

<script setup>
defineProps({
  sources: {
    type: Array,
    default: () => []
  }
})
</script>
