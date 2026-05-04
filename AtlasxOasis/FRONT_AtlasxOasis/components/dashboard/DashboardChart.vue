<template>
  <div class="bg-gradient-to-br from-[#1a3d2c] to-[#162e22] border border-secondary/20 rounded-xl p-8 space-y-8">
    <!-- Titre -->
    <div>
      <h2 class="font-title text-2xl text-[#E9EEEC] mb-2">Statistiques des réservations</h2>
      <p class="text-muted text-sm">Vue d'ensemble de cette semaine</p>
    </div>

    <!-- Graphique des réservations -->
    <div class="space-y-4">
      <h3 class="font-title text-[11px] font-semibold text-[#E9EEEC]/70 uppercase tracking-wider">Réservations par jour</h3>
      
      <!-- Conteneur du graphique -->
      <div class="bg-secondary/5 border border-secondary/20 rounded-lg p-8 max-md:overflow-x-auto">
        <div class="flex items-end justify-between h-80 gap-3">
          <div v-for="day in weekData" :key="day.name" class="flex-1 flex flex-col items-center gap-2">
            <!-- Barre -->
            <div
              class="w-full bg-gradient-to-t from-accent to-primary rounded-t-lg transition-all duration-300 hover:opacity-80 hover:shadow-lg"
              :style="{ height: (day.value / maxValue * 320) + 'px' }"
            />

            <!-- Label jour + valeur -->
            <p class="text-[10px] text-[#E9EEEC]/40">{{ day.value }}</p>
            <p class="text-[11px] font-semibold text-[#E9EEEC]/70">{{ day.name }}</p>
          </div>
        </div>

        <!-- Échelle Y -->
        <div class="mt-4 pt-4 border-t border-secondary/20 flex justify-between text-[10px] text-muted">
          <span>0</span>
          <span>{{ (maxValue / 2).toFixed(0) }}</span>
          <span>{{ maxValue }}</span>
        </div>
      </div>
    </div>

    <!-- KPIs -->
    <div class="grid grid-cols-3 gap-4 pt-6 border-t border-secondary/20 max-md:flex max-md:flex-col">
      <div class="space-y-2">
        <p class="text-muted text-[11px] uppercase tracking-wider">Participants totaux</p>
        <p class="font-title text-2xl text-accent">{{ stats.totalParticipants }}</p>
        <p class="text-[10px] text-green-400">↑ +12% vs semaine</p>
      </div>

      <div class="space-y-2">
        <p class="text-muted text-[11px] uppercase tracking-wider">Revenus</p>
        <p class="font-title text-2xl text-accent">{{ stats.revenue }}€</p>
        <p class="text-[10px] text-green-400">↑ +8% vs semaine</p>
      </div>

      <div class="space-y-2">
        <p class="text-muted text-[11px] uppercase tracking-wider">Taux remplissage</p>
        <p class="font-title text-2xl text-accent">{{ stats.fillRate }}%</p>
        <p class="text-[10px] text-green-400">↑ Excellent</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useDashboard } from '~/composables/useDashboard'

const { weekData, totalParticipants, totalRevenue, fillRate, loading, fetchStats } = useDashboard()

const stats = computed(() => ({
  totalParticipants: totalParticipants.value,
  revenue: Math.round(totalRevenue.value),
  fillRate: fillRate.value,
}))

const maxValue = computed(() => {
  const max = Math.max(...weekData.value.map(d => d.value))
  return max > 0 ? max : 1
})

onMounted(() => fetchStats())
</script>
