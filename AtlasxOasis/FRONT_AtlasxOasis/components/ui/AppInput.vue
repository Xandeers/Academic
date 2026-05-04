<template>
  <div class="flex flex-col gap-1.5 w-full">
    <label v-if="label" class="font-title text-[9px] tracking-[0.14em] uppercase text-accent/80">
      {{ label }}
    </label>
    <div
      class="bg-s1 border rounded-lg transition-colors duration-200"
      :class="error ? 'border-red-500/50' : 'border-white/10 focus-within:border-white/20'"
    >
      <input
        v-bind="$attrs"
        :type="type || 'text'"
        :placeholder="placeholder"
        :value="modelValue"
        :disabled="disabled"
        class="w-full bg-transparent border-none outline-none px-4 py-3 text-xs text-[#E9EEEC] placeholder:text-muted"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
    </div>
    <span v-if="error" class="text-[11px] text-red-400">{{ error }}</span>
  </div>
</template>

<script setup lang="ts">
defineOptions({ inheritAttrs: false })
defineProps<{
  modelValue?: string
  label?: string
  placeholder?: string
  type?: string
  error?: string
  disabled?: boolean
}>()
defineEmits(['update:modelValue'])
</script>