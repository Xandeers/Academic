<template>
  <span class="inline-flex items-center gap-1.5 text-[10px] font-semibold" :class="variants[variant]">
    <span class="w-1.5 h-1.5 rounded-full bg-current" />
    <slot />
  </span>
</template>

<script setup lang="ts">
defineProps<{
  variant: 'published' | 'full' | 'draft' | 'cancelled'
}>()

const variants = {
  published: 'text-accent',
  full:      'text-primary',
  draft:     'text-muted',
  cancelled: 'text-red-400',
}
</script>