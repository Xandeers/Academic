<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-200"
      enter-from-class="opacity-0"
      leave-active-class="transition duration-200"
      leave-to-class="opacity-0"
    >
      <div
        v-if="modelValue"
        class="fixed inset-0 bg-black/75 backdrop-blur-md flex items-center justify-center z-50 p-5"
        @click.self="$emit('update:modelValue', false)"
      >
        <div class="bg-s1 border border-white/20 rounded-2xl w-full max-w-md shadow-[0_24px_80px_rgba(0,0,0,0.6)]">
          <div v-if="title" class="flex items-center justify-between px-6 pt-5">
            <h3 class="font-title text-base text-white">{{ title }}</h3>
            <button
              class="text-muted hover:text-white transition-colors px-2 py-1 rounded"
              @click="$emit('update:modelValue', false)"
            >✕</button>
          </div>
          <div class="px-6 py-5 text-[13px] text-white/65 leading-relaxed">
            <slot />
          </div>
          <div v-if="!hideFooter" class="flex gap-2.5 justify-end px-6 pb-5">
            <AppButton variant="ghost" @click="$emit('update:modelValue', false)">
              {{ cancelLabel ?? 'Annuler' }}
            </AppButton>
            <AppButton variant="primary" :loading="loading" @click="$emit('confirm')">
              {{ confirmLabel ?? 'Confirmer' }}
            </AppButton>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: boolean
  title?: string
  confirmLabel?: string
  cancelLabel?: string
  hideFooter?: boolean
  loading?: boolean
}>()
defineEmits(['update:modelValue', 'confirm'])
</script>