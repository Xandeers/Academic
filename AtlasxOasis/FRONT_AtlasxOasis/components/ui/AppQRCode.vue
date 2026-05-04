<template>
  <div class="app-qr-code">
    <img
      v-if="qrUrl"
      :src="qrUrl"
      :alt="alt"
      class="app-qr-code__img"
      @error="onImageError"
    />
    <div v-else class="app-qr-code__placeholder">
      <span class="text-muted text-xs">Impossible de charger le QR Code</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  value: string
  size?: number
  alt?: string
}>()

const emit = defineEmits<{
  error: []
}>()

// Génère l'URL du QR code avec l'API qr-server
const qrUrl = computed(() => {
  if (!props.value) return null
  const size = props.size || 200
  // Encode la valeur pour l'URL
  const encodedValue = encodeURIComponent(props.value)
  return `https://api.qrserver.com/v1/create-qr-code/?size=${size}x${size}&data=${encodedValue}`
})

const onImageError = () => {
  emit('error')
}
</script>

<style scoped>
.app-qr-code {
  display: flex;
  align-items: center;
  justify-content: center;
}

.app-qr-code__img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  border: 1px solid rgba(153, 215, 184, 0.12);
  padding: 8px;
  background: white;
}

.app-qr-code__placeholder {
  width: 100%;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(153, 215, 184, 0.05);
  border: 1px dashed rgba(153, 215, 184, 0.2);
  border-radius: 8px;
}
</style>
