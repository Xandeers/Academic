<template>
  <!-- Event card container -->
  <div         
    class="bg-s1 border border-white/5 rounded-2xl overflow-hidden cursor-pointer hover:border-white/10 hover:-translate-y-1 hover:shadow-2xl transition-all duration-200"
    @click="navigateTo(`/events/${event.id_event}`)"
  >
    <!-- Event card tag + likes + gradient container -->
    <div :class="['h-36 flex items-start justify-between p-3', randomColor]">
      <span class="text-[9px] font-title tracking-widest text-accent bg-accent/10 border border-accent/20 rounded-full px-3 py-1">
        {{ event.category?.[0]?.name ?? event.category?.[0]?.label ?? '' }}
      </span>
      <div class="flex items-center gap-1 text-[#E9EEEC]/40 text-xs">
        <Heart :size="11" /> {{ event.like_count }}
      </div>
    </div>

    <!-- Event footer container -->
    <div class="p-4 flex flex-col gap-2">
      <div class="font-title text-sm text-[#E9EEEC] leading-snug">{{ event.title }}</div>
      <div class="text-xs text-muted">{{ getDateFromTimestamp(event.begin_date) }}</div>

      <!-- Event price + availability container -->
      <div class="flex items-center gap-2 mt-1">
        <span class="font-title text-base text-accent">{{ event.price === 0 ? 'Gratuit' : `${event.price} €` }}</span>

        <div class="flex-1 h-0.5 bg-primary/10 rounded-full overflow-hidden">
          <EventProgressBar :reserved="event.reserved" :capacity="event.capacity"></EventProgressBar>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Event } from '~/types/event'
import { Search, Heart } from 'lucide-vue-next'

const props = defineProps(['event'])
const randomColor = ref('')

defineEmits(['click', 'join'])
function formatDate(d: string) {
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' })
}

const colors = [
  'bg-[linear-gradient(135deg,#0d1f2d,#1a2e3d)]',
  'bg-[linear-gradient(135deg,#130d2d,#1f1a3d)]',
  'bg-[linear-gradient(135deg,#1f0d0d,#2e1a1a)]',
  'bg-[linear-gradient(135deg,#0d1f10,#1a2e1e)]',
  'bg-[linear-gradient(135deg,#1a1f0d,#2a2e1a)]',
  'bg-[linear-gradient(135deg,#1f1a0d,#2e261a)]',
  'bg-[linear-gradient(135deg,#0d1a2d,#1a263d)]',
  'bg-[linear-gradient(135deg,#1a0d2d,#261a3d)]'
]

onMounted(() => {
  randomColor.value = colors[Math.floor(Math.random() * colors.length)]
})
</script>
