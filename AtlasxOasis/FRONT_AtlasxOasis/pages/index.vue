<template>
  <div class="min-h-screen bg-bg text-white flex flex-col">

    <!-- NAV -->
    <nav class="sticky top-0 z-50 flex items-center justify-between px-10 py-5 bg-bg/85 backdrop-blur-xl border-b border-white/5">
      <span class="font-title text-accent text-lg tracking-wide" style="text-shadow:0 0 16px rgba(56,227,143,0.3)">AtlasXOasis</span>
      <div class="flex items-center gap-3 max-md:flex-col">
        <NuxtLink to="/events" class="text-[13px] text-white/50 hover:text-primary transition-colors no-underline">Explorer</NuxtLink>
        <NuxtLink to="/auth/login" class="px-4 py-2 rounded-lg border border-secondary/30 text-[12px] font-semibold text-primary hover:bg-secondary/10 transition-colors no-underline">Connexion</NuxtLink>
        <NuxtLink to="/auth/register" class="px-4 py-2 rounded-lg bg-accent text-[#0b2618] font-title text-[12px] hover:shadow-[0_0_20px_rgba(56,227,143,0.35)] transition-all no-underline">S'inscrire</NuxtLink>
      </div>
    </nav>

    <!-- HERO -->
    <section class="relative flex justify-center px-10 py-20 overflow-hidden">
      <div class="absolute w-[600px] h-[600px] rounded-full bg-accent/5 blur-[100px] -top-40 left-1/2 -translate-x-1/2 pointer-events-none" />
      <div class="relative flex flex-col items-center gap-6 max-w-2xl w-full text-center">
        <div class="inline-flex items-center gap-2 text-[11px] font-semibold text-accent bg-accent/8 border border-accent/20 rounded-full px-4 py-1.5">
          <span class="w-1.5 h-1.5 rounded-full bg-accent shadow-[0_0_8px_rgba(56,227,143,1)] animate-pulse" />
          2 400+ événements disponibles
        </div>
        <h1 class="font-title text-5xl leading-[1.05] tracking-tight">
          Trouvez votre<br>
          <span class="bg-gradient-to-r from-accent to-primary bg-clip-text text-transparent">prochain événement</span>
        </h1>
        <div class="flex items-center w-full bg-white/5 border border-white/15 rounded-xl overflow-hidden focus-within:border-accent/40 transition-colors">
          <span class="px-4 text-muted">🔍</span>
          <input
            v-model="searchQuery"
            placeholder="Concert, festival, atelier, ville…"
            class="flex-1 bg-transparent border-none outline-none py-4 font-body text-[14px] text-white placeholder:text-muted"
            @keydown.enter="goSearch"
          />
          <button
            class="bg-accent text-[#0b2618] px-6 py-4 font-title text-[12px] tracking-wider hover:bg-primary transition-colors"
            @click="goSearch"
          >
            Explorer
          </button>
        </div>
        <div class="flex gap-2 flex-wrap justify-center">
          <button
            v-for="cat in categories"
            :key="cat.name"
            class="flex items-center gap-1.5 px-4 py-2 rounded-full bg-s1 border border-white/10 text-[12px] text-muted hover:border-white/20 hover:text-primary transition-all"
            @click="goCategory(cat.name)"
          >
            <component :is="cat.icon" :size="13" />
            {{ cat.name }}
          </button>
        </div>
      </div>
    </section>

    <!-- KPI STATS -->
    <section class="px-10 pb-10">
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
    </section>

    <!-- ÉVÉNEMENTS -->
    <section class="px-10 pb-10 flex flex-col gap-5">
      <div class="flex items-center justify-between">
        <span class="font-title text-xl">Tendances</span>
        <NuxtLink to="/events" class="text-[12px] font-semibold text-primary hover:text-accent transition-colors no-underline">Voir tout →</NuxtLink>
      </div>
  
      <div v-if="error" class="text-red-400 text-sm">
        Impossible de charger les événements pour le moment.
      </div>

      <EventGrid v-else-if="events && events.length" :events="events"></EventGrid>
    </section>

    <!-- BANNER -->
    <section class="mx-10 mb-10 relative overflow-hidden bg-gradient-to-br from-[#1a3d2c] to-[#0f2018] border border-secondary/35 rounded-2xl p-12 flex items-center justify-between gap-10 max-md:flex max-md:flex-col">
      <div class="absolute w-[500px] h-[500px] rounded-full bg-accent/5 blur-[80px] -right-40 -top-40 pointer-events-none" />
      <div class="relative flex flex-col gap-4">
        <span class="font-title text-[9px] tracking-[0.18em] uppercase text-accent opacity-80">Vous organisez ?</span>
        <h2 class="font-title text-3xl leading-snug">Créez votre événement<br>en 5 minutes</h2>
        <p class="text-[13px] text-white/50 leading-relaxed max-w-md">Publiez, gérez vos billets et suivez vos participants en temps réel.</p>
        <NuxtLink to="/auth/register" class="inline-flex w-fit bg-accent text-[#0b2618] font-title text-[11px] tracking-wider px-6 py-3 rounded-lg hover:shadow-[0_0_24px_rgba(56,227,143,0.35)] transition-all no-underline">
          Commencer gratuitement →
        </NuxtLink>
      </div>
      <div class="relative flex gap-10 flex-shrink-0">
        <div v-for="s in stats" :key="s.label" class="text-center">
          <component :is="s.icon" :size="22" class="text-accent mx-auto mb-2" />
          <div class="font-title text-3xl text-accent">{{ s.getValue() }}+</div>
          <div class="text-[11px] text-muted mt-1">{{ s.label }}</div>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import { Search, Music, Dumbbell, Palette, Gamepad2, Wrench, Film, CalendarDays, Users, Building2, DollarSign } from 'lucide-vue-next'
import { useDashboard } from '~/composables/useDashboard'

const iconMap = {
  'Musique': Music,
  'Sport': Dumbbell,
  'Culture': Palette,
  'E-Sport': Gamepad2,
  'Ateliers': Wrench,
  'Cinéma': Film,
}

const { totalEvents, totalParticipants, totalRevenue, totalOrganizers, fetchStats } = useDashboard()

onMounted(() => fetchStats())

const store = useEventsStore()
const { searchQuery, activeFilter } = storeToRefs(store)

await callOnce(store.fetchEvents)

const events = store.events

const { data: categoriesList } = await useFetch('/api/category/', {
  server: false, 
  key: 'home-categories-list'
})

const categories = computed(() => {
  const apiData = categoriesList.value || []

  const mapped = apiData.map(cat => ({
    name: cat.label,
    id: cat.id_category,
    icon: iconMap[cat.label]
  }))

  return mapped
})

definePageMeta({ layout: false })
// const searchQuery = ref('')
function goSearch() {
  navigateTo(searchQuery.value.trim() ? `/events?q=${searchQuery.value}` : '/events')
}

function goCategory(name) {
  activeFilter.value = name
  navigateTo(`/events?f=${name}`)
}

const stats = [
  { getValue: () => totalEvents.value,       label: 'Événements',   icon: CalendarDays },
  { getValue: () => totalParticipants.value, label: 'Participants',  icon: Users },
  { getValue: () => totalOrganizers.value,   label: 'Organisateurs', icon: Building2 },
]
</script>