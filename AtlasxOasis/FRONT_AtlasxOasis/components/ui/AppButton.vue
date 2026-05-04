<template>
  <button
    v-bind="$attrs"
    :disabled="disabled || loading"
    :class="[
      'inline-flex items-center justify-center gap-2 rounded-lg px-5 py-2.5',
      'font-title text-[11px] tracking-widest uppercase transition-all duration-200',
      'disabled:opacity-40 disabled:cursor-not-allowed whitespace-nowrap',
      variants[variant ?? 'primary']
    ]"
  >
    <span
      v-if="loading"
      class="w-3.5 h-3.5 border-2 border-white/25 border-t-current rounded-full animate-spin"
    />
    <slot />
  </button>
</template>

<script setup lang="ts">
defineOptions({ inheritAttrs: false })

defineProps<{
  variant?: 'primary' | 'ghost' | 'danger' | 'dark'
  disabled?: boolean
  loading?: boolean
}>()

const variants = {
  primary: 'bg-accent text-[#0b2618] shadow-[0_4px_20px_rgba(56,227,143,0.2)] hover:shadow-[0_0_24px_rgba(56,227,143,0.4)] hover:-translate-y-px',
  ghost:   'bg-transparent text-primary border border-secondary/40 hover:bg-secondary/10',
  danger:  'bg-red-500/10 text-red-400 border border-red-500/25 hover:text-white hover:bg-red-500',
  dark:    'bg-gradient-to-br from-[#1a3d2c] to-[#162e22] text-white/60 border border-secondary/35 hover:text-primary',
}
</script>