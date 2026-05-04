<template>
  <div class="flex flex-col gap-1.5 w-full">
    <label v-if="label" class="font-title text-[9px] tracking-[0.14em] uppercase text-accent/80">
      {{ label }}
    </label>
    <div class="relative bg-s1 border border-white/10 rounded-lg focus-within:border-white/20 transition-colors">
      <select
        :value="modelValue"
        :disabled="disabled"
        class="w-full bg-transparent border-none outline-none px-4 py-3 pr-10 font-body text-xs text-white appearance-none cursor-pointer"
        @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
      >
        <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
        <option v-for="opt in options" :key="opt.value" :value="opt.value" class="bg-s2">
          {{ opt.label }}
        </option>
      </select>
      <span class="absolute right-3.5 top-1/2 -translate-y-1/2 text-muted pointer-events-none">▾</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue?: string
  label?: string
  placeholder?: string
  options: { value: string; label: string }[]
  disabled?: boolean
}>()
defineEmits(['update:modelValue'])
</script>