<template>
  <div class="flex flex-col gap-1.5">
    <div class="flex justify-between items-center">
      <span class="text-[10px] text-muted">Disponibilité</span>
      <span
        class="text-[10px] font-title"
        :class="{
          'text-accent':     pct < 50,
          'text-orange-400': pct >= 50 && pct < 80,
          'text-red-400':    pct >= 80
        }"
      >
        {{ remaining }} place{{ remaining > 1 ? 's' : '' }} restante{{ remaining > 1 ? 's' : '' }}
      </span>
    </div>
    <EventProgressBar :reserved="reserved" :capacity="capacity"></EventProgressBar>
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