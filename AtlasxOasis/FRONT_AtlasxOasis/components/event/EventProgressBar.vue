<template>
  <div class="flex flex-col gap-1.5">
    <div class="h-1.5 bg-primary/10 rounded-full overflow-hidden">
      <div
        class="h-full rounded-full transition-all duration-500"
        :class="{
          'bg-accent':     pct < 50,
          'bg-orange-400': pct >= 50 && pct < 80,
          'bg-red-400':    pct >= 80
        }"
        :style="{ width: `${pct}%` }"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  reserved: number
  capacity: number
}>()

const pct = computed(() =>
  Math.round((props.reserved / props.capacity) * 100)
)

const remaining = computed(() =>
  props.capacity - props.reserved
)
</script>