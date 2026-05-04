<template>
  <!-- Page container -->
  <div>
    <div>
      <h1 class="font-title mb-1">Liste des organisateurs référencés</h1>
      <div>
        <div
          v-for="organizer in organizers ?? []"
          :key="organizer.id_organizer"
          class="p-6 mb-6 bg-s1 border border-white/5 rounded-2xl flex flex-row justify-between items-center"
        >
          <div 
            class="text-sm font-semibold text-[#E9EEEC] hover:underline hover:cursor-pointer"
            @click="navigateTo(`/organizers/${organizer.id_organizer}`)"
          >
            {{ organizer.username }}
          </div>
          <button
            :class="[
              'ml-auto px-4 py-1.5 rounded-lg border text-xs transition-all',
              'bg-secondary/15 border-secondary/25 text-accent hover:bg-secondary/25'
            ]"
            @click="navigateTo(`/organizers/${organizer.id_organizer}`)"
          >
            {{ "Voir plus +" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({layout: 'default'})

const organizers = await $fetch("/api/organizers/")

</script>