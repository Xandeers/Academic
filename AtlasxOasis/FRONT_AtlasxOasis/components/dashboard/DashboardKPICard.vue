<template>
  <div class="bg-gradient-to-br from-[#1a3d2c] to-[#162e22] border border-secondary/20 rounded-xl p-5 flex flex-col gap-4 transition-all duration-300 hover:border-secondary/40 hover:shadow-[0_8px_24px_rgba(56,227,143,0.15)] hover:-translate-y-0.5">
    <!-- En-tête : icône + titre -->
    <div class="flex items-center gap-3">
      <div class="text-accent flex-shrink-0">
        <component :is="dynamicIcon as any" />
      </div>
      <h3 class="font-title text-[11px] font-semibold text-[#E9EEEC]/70 uppercase tracking-wider">{{ title }}</h3>
    </div>

    <!-- Valeur principale -->
    <div class="font-title text-3xl font-black text-accent leading-tight">{{ formattedValue }}</div>

    <!-- Trend (évolution) -->
    <div :class="['flex items-center gap-1.5 text-[11px] font-semibold', trend === 'positif' ? 'text-green-500' : 'text-red-500']">
      <TrendingUp v-if="trend === 'positif'" :size="14" class="flex-shrink-0" />
      <TrendingDown v-else :size="14" class="flex-shrink-0" />
      <span>{{ trend === 'positif' ? '↑ En hausse' : '↓ En baisse' }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import * as Icons from 'lucide-vue-next'
import { TrendingUp, TrendingDown } from 'lucide-vue-next'

const props = defineProps<{
  title: string
  value: number
  icon: keyof typeof Icons
  trend: 'positif' | 'négatif'
}>()

// Récupère l'icône dynamiquement
const dynamicIcon = computed(() => {
  return Icons[props.icon] || Icons.Activity
})

// Formate la valeur avec séparateurs de milliers
const formattedValue = computed(() => {
  return props.value.toLocaleString('fr-FR')
})
</script>
