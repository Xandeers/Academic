<template>
  <!-- Grid container -->
  <div class="grid grid-cols-4 gap-4 max-md:flex max-md:flex-col">
    <div
      v-for="event in events"
      :key="event.id_event"
      class="bg-s1 border border-white/5 rounded-2xl overflow-hidden cursor-pointer hover:border-white/10 hover:-translate-y-1 hover:shadow-2xl transition-all duration-200"
      @click="navigateTo(`/events/${event.id_event}`)"
    >
      <EventCard :event="event"></EventCard>
    </div>
  </div>
</template>	

<script setup lang="ts">
import type { Event } from '~/types/event';
const props = defineProps(['events']);
</script>