<template>
  <span
    :class="[
      'inline-flex items-center gap-1.5 text-[10px] font-title tracking-widest px-3 py-1 rounded-full border',
      styles[status]
    ]"
  >
    <span :class="['w-1.5 h-1.5 rounded-full', dotStyles[status]]" />
    {{ labels[status] }}
  </span>
</template>

<script setup lang="ts">
defineProps<{
  status: 'published' | 'full' | 'draft' | 'cancelled'
}>()

const styles = {
  published: 'bg-accent/10 border-accent/20 text-accent',
  full:      'bg-orange-500/10 border-orange-500/20 text-orange-400',
  draft:     'bg-white/5 border-white/10 text-muted',
  cancelled: 'bg-red-500/10 border-red-500/20 text-red-400',
}

const dotStyles = {
  published: 'bg-accent shadow-[0_0_6px_rgba(56,227,143,0.6)]',
  full:      'bg-orange-400',
  draft:     'bg-muted',
  cancelled: 'bg-red-400',
}

const labels = {
  published: 'Publié',
  full:      'Complet',
  draft:     'Brouillon',
  cancelled: 'Annulé',
}
</script>