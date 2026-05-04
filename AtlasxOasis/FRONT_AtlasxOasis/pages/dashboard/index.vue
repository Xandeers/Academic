<template>
  <div class="min-h-screen bg-bg text-[#E9EEEC] flex flex-col">
    <!-- NAV -->
    <nav class="sticky top-0 z-50 flex items-center justify-between px-10 py-5 bg-bg/85 backdrop-blur-xl border-b border-white/5">
      <NuxtLink to="/" class="font-title text-accent text-lg tracking-wide no-underline hover:text-primary transition-colors">
        ← Accueil
      </NuxtLink>
      <h1 class="font-title text-xl">Dashboard</h1>
      <div class="w-32"></div>
    </nav>

    <!-- CONTENT -->
    <section class="flex-1 px-10 py-8 space-y-8">
      <!-- KPI Cards -->
      <div class="grid grid-cols-4 gap-6 max-md:flex max-md:flex-col">
        <DashboardKPICard
          title="Événements"
          :value="totalEvents"
          icon="CalendarDays"
          trend="positif"
        />
        <DashboardKPICard
          title="Participants"
          :value="totalParticipants"
          icon="Users"
          trend="positif"
        />
        <DashboardKPICard
          title="Organisateurs"
          :value="totalOrganizers"
          icon="Building2"
          trend="positif"
        />
        <DashboardKPICard
          title="Revenus"
          :value="Math.round(totalRevenue)"
          icon="DollarSign"
          trend="positif"
        />
      </div>

      <!-- Statistiques Chart -->
      <DashboardChart />
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useDashboard } from '~/composables/useDashboard'

definePageMeta({ 
  layout: 'default',
  middleware: 'auth'
})
const { totalEvents, totalParticipants, totalRevenue, totalOrganizers, fetchStats } = useDashboard()

onMounted(() => fetchStats())
</script>
