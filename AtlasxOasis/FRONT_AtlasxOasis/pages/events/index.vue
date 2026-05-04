<template>
  <div class="min-h-screen bg-bg">
    <section class="px-10 py-16 text-center flex flex-col items-center gap-6">
      <h1 class="font-title text-5xl text-[#E9EEEC]">Explorer les événements</h1>
      <div class="flex items-center gap-2 bg-s1 border border-white/5 rounded-xl px-4 py-3 w-full max-w-xl focus-within:border-accent/40 transition-colors">
        <Search :size="16" class="text-muted shrink-0" />
        <input
          v-model="searchQuery"
          placeholder="Concert, festival, ville…"
          class="bg-transparent text-sm text-[#E9EEEC] placeholder-muted outline-none flex-1 font-body"
        />
      </div>
      <div class="flex gap-2 flex-wrap justify-center">
        <button
          v-for="cat in categories"
          :key="cat"
          :class="['flex items-center gap-1.5 px-4 py-2 rounded-full border text-xs font-title transition-all', activeFilter === cat ? 'bg-accent/10 border-accent/30 text-accent' : 'bg-s1 border-white/5 text-muted hover:border-white/10 hover:text-primary']"
          @click="activeFilter = cat"
        >
          {{ cat }}
        </button>
      </div>
    </section>

    <section class="px-10 pb-16">      
      <EventGrid :events="filteredEvents"></EventGrid>
      <div v-if="filteredEvents.length === 0" class="text-center text-muted py-20 text-sm">
        Aucun événement trouvé.
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { Search, Heart } from 'lucide-vue-next'
// import { eventTests } from '~/mocks/events'
import { storeToRefs } from 'pinia'

const store = useEventsStore()

const { data } = await useFetch("/api/events/")
if (data.value) {
  store.events = data.value
}

const { data: categoriesList } = await useFetch('/api/category/')
const categoriesAux = categoriesList.value?.map(obj => obj.label) || []

const categories = ['Tout', ...categoriesAux]

const { searchQuery, activeFilter, filteredEvents } = storeToRefs(store)
</script>