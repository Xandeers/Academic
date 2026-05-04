<template>
  <div class="p-8 bg-bg min-h-screen">
    <div class="max-w-2xl mx-auto">
      <div class="mb-8">
        <h1 class="text-3xl font-title text-accent mb-2">Test BookingForm</h1>
        <p class="text-muted">Testez le formulaire de réservation avec un événement mock</p>
      </div>

      <BookingForm :event="mockEvent" @success="onSuccess" @error="onError" />

      <!-- Logs -->
      <div v-if="logs.length > 0" class="mt-8 p-6 bg-s1 border border-white/10 rounded-lg">
        <h2 class="text-lg font-title text-accent mb-4">Logs</h2>
        <div class="space-y-2 max-h-64 overflow-y-auto">
          <div v-for="(log, idx) in logs" :key="idx" :class="[
            'p-3 rounded text-sm font-mono',
            log.type === 'success' ? 'bg-green-500/10 text-green-400 border border-green-500/25' :
            log.type === 'error' ? 'bg-red-500/10 text-red-400 border border-red-500/25' :
            'bg-blue-500/10 text-blue-400 border border-blue-500/25'
          ]">
            [{{ log.type.toUpperCase() }}] {{ log.message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Event } from '~/types/event'
import BookingForm from '~/components/booking/BookingForm.vue'

interface Log {
  type: 'success' | 'error' | 'info'
  message: string
}

const logs = ref<Log[]>([])

const mockEvent: Event = {
  id: 'evt_123',
  title: 'Concert Premium 2026',
  description: 'Un super concert en plein air',
  category: 'Musique',
  status: 'published',
  date: '2026-04-15',
  time: '20:00',
  location: 'Paris - Stade de France',
  price: 50,
  capacity: 500,
  reserved: 200,
  organizer: {
    id: 'org_1',
    name: 'Live Events Pro',
    certified: true,
    followersCount: 1000
  },
  tags: [
    { id: 'tag1', label: 'Live' },
    { id: 'tag2', label: 'Popular' }
  ],
  ticketTypes: [
    {
      id: 'tk1',
      label: 'Standard',
      price: 50,
      description: 'Accès général aux gradins',
      available: 100
    },
    {
      id: 'tk2',
      label: 'VIP',
      price: 100,
      description: 'Front row + cocktail gratuit',
      available: 50
    },
    {
      id: 'tk3',
      label: 'Étudiant',
      price: 25,
      description: 'Tarif réduit avec justificatif',
      available: 75
    },
    {
      id: 'tk4',
      label: 'Family Pack (4 places)',
      price: 150,
      description: 'Pour toute la famille',
      available: 25
    }
  ],
  likesCount: 250,
  createdAt: new Date().toISOString()
}

const onSuccess = (booking: any) => {
  const message = `✅ Réservation créée - ID: ${booking.id} | ${booking.quantity} place(s) | ${booking.totalPrice}€`
  logs.value.unshift({ type: 'success', message })
  console.log('Booking créé:', booking)
}

const onError = (message: string) => {
  logs.value.unshift({ type: 'error', message: `❌ ${message}` })
  console.error('Erreur:', message)
}
</script>
