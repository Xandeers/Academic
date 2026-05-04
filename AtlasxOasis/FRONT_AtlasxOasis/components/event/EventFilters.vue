<template>
  <div class="event-filters">
    <button
      v-for="cat in categories" :key="cat"
      class="filter-pill" :class="{ 'filter-pill--on': modelValue === cat }"
      @click="$emit('update:modelValue', cat)"
    >
      {{ cat }}
    </button>
  </div>
</template>

<script setup lang="ts">
import type { EventCategory } from '~/types/event'
defineProps<{ modelValue: EventCategory | 'Tout' }>()
defineEmits(['update:modelValue'])
const categories: (EventCategory | 'Tout')[] = ['Tout','Musique','Sport','Culture','E-Sport','Ateliers','Cinéma']
</script>

<style scoped>
.event-filters { display: flex; gap: 8px; flex-wrap: wrap; }
.filter-pill {
  padding: 7px 16px; border-radius: 20px; font-size: 11px; font-weight: 600;
  letter-spacing: 0.04em; border: 1px solid var(--border); color: var(--muted);
  cursor: pointer; background: var(--s1); transition: all 0.18s;
}
.filter-pill--on { background: rgba(56,227,143,0.12); border-color: rgba(56,227,143,0.3); color: var(--accent); }
.filter-pill:hover:not(.filter-pill--on) { border-color: var(--border2); color: var(--primary); }
</style>