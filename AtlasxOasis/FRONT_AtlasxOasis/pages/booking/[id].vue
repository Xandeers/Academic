<template>
  <div class="min-h-screen bg-background px-5 py-10">

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-24 px-5">
      <div class="w-10 h-10 mx-auto mb-5 border-4 border-accent/20 border-t-accent rounded-full animate-spin" />
      <p class="text-muted">Chargement de votre réservation...</p>
    </div>

    <!-- Success -->
    <template v-else-if="lastBooking && tickets.length > 0">
      <!-- Success Header -->
      <div class="text-center mb-16">
        <div class="w-20 h-20 mx-auto mb-6 bg-accent/20 border-4 border-accent rounded-full flex items-center justify-center text-5xl text-accent font-bold">
          ✓
        </div>
        <h1 class="font-title text-4xl font-black text-white uppercase tracking-wide mb-3">
          Réservation Confirmée !
        </h1>
        <p class="text-base text-primary max-w-2xl mx-auto">
          Votre billet numérique est prêt. Consultez-le ci-dessous.
        </p>
      </div>

      <!-- Booking Summary -->
      <div class="max-w-4xl mx-auto flex flex-col gap-10">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 p-6 bg-gradient-to-br from-s1 to-s2 border border-accent/10 rounded-xl">
          <div class="flex flex-col gap-2">
            <span class="text-xs tracking-wider uppercase text-muted font-semibold">Référence</span>
            <span class="text-base font-bold text-white font-mono">#{{ lastBooking.id_event }}-{{ lastBooking.id_ticket_type }}</span>
          </div>
          <div class="flex flex-col gap-2">
            <span class="text-xs tracking-wider uppercase text-muted font-semibold">Statut</span>
            <span class="text-base font-bold text-white">
              <span v-if="lastBooking.status_ticket === 'confirmed' || lastBooking.status_ticket === null" class="text-accent">✓ Confirmé</span>
              <span v-else-if="lastBooking.status_ticket === 'pending'" class="text-yellow-400">⏱ En attente</span>
              <span v-else class="text-red-400">✗ Annulé</span>
            </span>
          </div>
          <div class="flex flex-col gap-2">
            <span class="text-xs tracking-wider uppercase text-muted font-semibold">Places</span>
            <span class="text-base font-bold text-white">{{ lastBooking.quantity }} {{ lastBooking.quantity > 1 ? 'places' : 'place' }}</span>
          </div>
          <div class="flex flex-col gap-2">
            <span class="text-xs tracking-wider uppercase text-muted font-semibold">Prix total</span>
            <span class="text-lg font-bold text-accent font-title">{{ totalPrice === 0 ? 'Gratuit' : `${totalPrice.toFixed(2)} €` }}</span>
          </div>
        </div>

        <!-- Tickets Grid -->
        <div class="flex flex-col gap-6">
          <h2 class="font-title text-2xl font-black text-white uppercase tracking-wide">Vos Billets</h2>
          <div class="grid grid-cols-1 gap-6">
            <BookingTicket
              v-for="(ticket, idx) in tickets"
              :key="ticket.id"
              :ticket="ticket"
              :showActions="idx === 0"
            />
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-md mx-auto w-full mt-4">
          <AppButton variant="primary" @click="shareBooking">
            📤 Partager
          </AppButton>
          <AppButton variant="ghost" @click="goToEvents">
            Voir d'autres événements
          </AppButton>
        </div>
      </div>
    </template>

    <!-- Error State -->
    <div v-else class="text-center py-24 px-5 max-w-md mx-auto">
      <div class="text-7xl mb-5">⚠</div>
      <h2 class="font-title text-2xl text-white mb-3">Réservation non trouvée</h2>
      <p class="text-muted mb-6">
        Impossible de charger votre réservation.
      </p>
      <AppButton variant="ghost" class="w-full" @click="goToEvents">
        Retour aux événements
      </AppButton>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import type { ApiBooking } from '~/types/booking'
import type { ApiEvent } from '~/types/event'
import BookingTicket from '~/components/booking/BookingTicket.vue'
import AppButton from '~/components/ui/AppButton.vue'

definePageMeta({ layout: 'default' })

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const eventId = route.params.id as string

// Récupérés depuis la page événement après création
const lastBooking = useState<ApiBooking | null>('last-booking', () => null)

// Charger les détails de l'événement pour afficher les billets
const { data: eventData } = await useFetch<ApiEvent>(`/api/events/${eventId}`, {
  server: false,
  key: `booking-event-${eventId}`,
})

const loading = ref(false)
const bookingNotFound = ref(false)

// Si pas de booking en state (accès direct, refresh), essayer de récupérer depuis my_bookings
onMounted(async () => {
  if (!lastBooking.value?.id_event) {
    loading.value = true
    try {
      const bookings = await $fetch<ApiBooking[]>('/api/bookings/my-bookings', {
        headers: { Authorization: `Bearer ${auth.token}` },
      })
      lastBooking.value = bookings.find(b => String(b.id_event) === eventId) ?? null
      if (!lastBooking.value) bookingNotFound.value = true
    } catch {
      bookingNotFound.value = true
    } finally {
      loading.value = false
    }
  }
})

// Construire les Ticket[] pour BookingTicket à partir du booking + event
const tickets = computed(() => {
  const b = lastBooking.value
  const e = eventData.value
  if (!b || !e) return []
  const qty = b.quantity ?? 1
  const pricePerTicket = (e.price ?? 0)
  return Array.from({ length: qty }, (_, i) => ({
    id: `${b.id_event}-${b.id_ticket_type}-${i + 1}`,
    bookingId: String(b.id_event),
    idTicketType: b.id_ticket_type,
    eventId: String(b.id_event),
    eventTitle: e.title ?? '',
    eventDate: e.begin_date ? new Date(e.begin_date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : '',
    eventTime: e.begin_date ? new Date(e.begin_date).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }) : '',
    eventLocation: '',
    eventCategory: e.category?.[0]?.name ?? e.category?.[0]?.label ?? '',
    holderName: auth.user?.username ?? '',
    ticketNumber: `ATX${String(b.id_event).padStart(6, '0')}${String(i + 1).padStart(3, '0')}`,
    ticketType: 'Standard',
    qrCodeData: `booking:event:${b.id_event}:ticket:${b.id_ticket_type}:${i + 1}`,
    price: pricePerTicket,
  }))
})

const totalPrice = computed(() => {
  const b = lastBooking.value
  const e = eventData.value
  if (!b || !e) return 0
  return (e.price ?? 0) * (b.quantity ?? 1)
})

const goToEvents = () => router.push('/events')

const shareBooking = async () => {
  const text = `J'ai réservé un billet pour ${eventData.value?.title ?? 'cet événement'} ! Référence : ${lastBooking.value?.id_event}-${lastBooking.value?.id_ticket_type}`
  if (navigator.share) {
    await navigator.share({ title: 'Ma réservation', text, url: window.location.href })
  } else {
    await navigator.clipboard.writeText(text)
  }
}
</script>