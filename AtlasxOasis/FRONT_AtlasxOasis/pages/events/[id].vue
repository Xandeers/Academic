<template>
  <div v-if="event">

    <!-- Breadcrumb -->
    <div class="flex items-center gap-2 px-10 pt-6 text-xs text-[#E9EEEC]/50">
      <NuxtLink to="/events" class="hover:text-primary transition-colors">Événements</NuxtLink>
      <span class="text-muted2">/</span>
      <span class="text-[#E9EEEC]/50">{{ event.category[0]?.name ?? event.category[0]?.label ?? 'Event' }}</span>
      <span class="text-muted2">/</span>
      <span class="text-primary">{{ event.title }}</span>
    </div>

    <!-- Hero -->
    <div class="relative mx-10 mt-4 rounded-2xl overflow-hidden h-64">
      <!-- <img v-if="event.image[0].url" :src="event.image[0].url" :alt="event.title" class="w-full h-full object-cover" />
      <div v-else class="w-full h-full bg-s2" /> -->
      <div class="w-full h-full bg-s2" />
      <div class="absolute inset-0 bg-gradient-to-t from-bg/90 via-bg/30 to-transparent flex flex-col justify-end p-7">
        <span class="inline-flex w-fit font-title text-[9px] tracking-widest text-accent bg-accent/12 border border-accent/25 rounded-full px-3 py-1 mb-3">
          {{ event.category[0]?.name ?? event.category[0]?.label ?? '' }} · Live
        </span>
        <h1 class="font-title text-3xl text-[#E9EEEC] leading-tight">{{ event.title }}</h1>
        <p class="text-xs text-[#E9EEEC]/50 mt-2">
          {{ getDateFromTimestamp(event.begin_date) }} · {{ getHourFromTimestamp(event.begin_date) }}
        </p>
      </div>
    </div>

    <!-- Body -->
    <div class="px-10 py-8 flex gap-6 items-start max-md:flex-col">

      <!-- Colonne principale -->
      <div class="flex-1 flex flex-col gap-5">

        <!-- Description -->
        <div class="bg-s1 border border-white/5 rounded-xl p-5">
          <h2 class="font-title text-sm text-[#E9EEEC] mb-3">À propos</h2>
          <p class="text-xs text-[#E9EEEC]/70 leading-relaxed">{{ event.description }}</p>
        </div>

        <!-- Organisateur -->
        <div class="bg-s1 border border-white/5 rounded-xl px-5 h-16 flex items-center gap-4">
          <div class="w-10 h-10 rounded-full bg-secondary/30 border border-secondary/40 flex items-center justify-center font-title text-sm text-accent flex-shrink-0">
            {{ event.organizer.username.substring(0, 2).toUpperCase() }}
          </div>
          <div class="flex flex-col gap-0.5">
            <div
              class="text-sm font-semibold text-[#E9EEEC] hover:underline hover:cursor-pointer"
              @click="navigateTo(`/organizers/${event.organizer.id_organizer}`)"
            >
              {{ event.organizer.username }}
            </div>
            <!-- <div class="text-xs text-muted">
              {{ event.organizer.certified ? 'Organisateur certifié' : 'Organisateur' }}
            </div> -->
          </div>
          <button
            :class="[
              'ml-auto px-4 py-1.5 rounded-lg border text-xs transition-all',
              isFollowing
                ? 'bg-secondary/25 border-secondary/40 text-primary'
                : 'bg-secondary/15 border-secondary/25 text-accent hover:bg-secondary/25'
            ]"
            @click="navigateTo(`/organizers/${event.organizer.id_organizer}`)"
          >
            {{ "Voir plus +" }}
          </button>
        </div>

          <!-- Tags -->
        <div class="flex gap-2 flex-wrap">
          <span
            v-for="tag in (event.tag ?? [])"
            :key="tag"
            class="px-3 py-1.5 bg-primary/5 border border-white/5 rounded-full text-xs text-muted"
          >
            {{ tag }}
          </span>
        </div>

      </div>

      <!-- Carte réservation -->
      <div class="w-72 flex-shrink-0 sticky top-24 bg-gradient-to-br from-[#1a3d2c] to-[#162e22] border border-secondary/35 rounded-2xl p-6 flex flex-col gap-4">

        <div class="font-title text-3xl text-accent">
          {{ event.price === 0 ? 'Gratuit' : `${event.price} €` }}
        </div>

        <div class="h-px bg-primary/10" />

        <div class="text-xs text-[#E9EEEC]/50 leading-7">
          Début : {{ getDateFromTimestamp(event.begin_date) }} · {{ getHourFromTimestamp(event.begin_date) }}<br />
          Fin : {{ getDateFromTimestamp(event.end_date) }} · {{ getHourFromTimestamp(event.end_date) }} <br />
          {{ event.reserved }} / {{ event.capacity }} places
        </div>

        <!-- Barre dispo -->
        <EventAvailability :reserved="event.reserved" :capacity="event.capacity ?? 0"></EventAvailability>

        <!-- Quantité -->
        <div class="flex items-center gap-4 text-xs text-[#E9EEEC]/50">
          <span>Quantité</span>
          <div class="flex items-center gap-3 bg-s2/50 border border-white/5 rounded-lg px-2 py-1">
            <button
              class="w-6 h-6 flex items-center justify-center text-primary hover:text-accent transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
              :disabled="qty <= 1"
              @click="qty--"
            >−</button>
            <span class="font-title text-sm text-[#E9EEEC] w-5 text-center">{{ qty }}</span>
            <button
              class="w-6 h-6 flex items-center justify-center text-primary hover:text-accent transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
              :disabled="qty >= maxQty"
              @click="qty++"
            >+</button>
          </div>
        </div>

        <!-- CTA -->
        <AppButton
          v-if="!isFull"
          variant="primary"
          class="w-full justify-center"
          :loading="bookingLoading"
          @click="handleReserve"
        >
          Réserver · {{ event.price === 0 ? 'Gratuit' : `${event.price * qty} €` }}
        </AppButton>
        <div v-else>
          <AppButton
            v-if="!userWaitlistPosition"
            variant="ghost"
            class="w-full justify-center"
            @click="handleWaitlist"
            :loading="waitlistLoading"
          >
            Liste d'attente
          </AppButton>
          <div v-else class="text-center p-3 bg-accent/10 border border-accent/20 rounded-lg">
            <p class="text-sm text-accent font-semibold">
              ✓ Position {{ userWaitlistPosition }} en liste d'attente
            </p>
            <button
              @click="leaveWaitlist(getWaitlistEntryForEvent(String(event?.id_event ?? ''))?.id || '')"
              class="text-xs text-muted hover:text-accent mt-2 transition-colors"
            >
              Se retirer
            </button>
          </div>
        </div>

        <!-- Erreur réservation -->
        <div v-if="bookingError" class="text-sm text-center p-3 rounded-lg border bg-red-500/10 text-red-400 border-red-500/25">
          {{ bookingError }}
        </div>

        <!-- Message de confirmation -->
        <div v-if="waitlistMessage" :class="[
          'text-sm text-center p-3 rounded-lg border',
          waitlistMessage.includes('✓')
            ? 'bg-green-500/10 text-green-400 border-green-500/25'
            : 'bg-red-500/10 text-red-400 border-red-500/25'
        ]">
          {{ waitlistMessage }}
        </div>

        <!-- Like / Favoris -->
        <button
          class="flex items-center justify-center gap-2 text-xs text-center transition-all duration-200 w-full py-2 rounded-lg border"
          :class="isFavorite
            ? 'text-accent border-accent/20 bg-accent/10'
            : 'text-[#E9EEEC]/35 border-white/5 hover:text-primary hover:border-white/10'"
          @click="toggleFavorite"
        >
          <Heart :size="13" :fill="isFavorite ? 'currentColor' : 'none'" />
          {{ isFavorite ? 'Liké' : 'Liker' }} · {{ likesCount }}
        </button>

        <!-- Partager -->
        <button
          class="flex items-center justify-center gap-2 text-xs text-center transition-all duration-200 w-full py-2 rounded-lg border border-white/5 text-[#E9EEEC]/35 hover:text-primary hover:border-white/10"
          @click="handleShare"
        >
          <Share2 :size="13" />
          {{ shareCopied ? 'Lien copié !' : 'Partager' }}
        </button>

        <AppButton
          variant="dark"
          class="w-full justify-center"
          @click="generateICS(event)"
        >
          Ajouter au calendrier
        </AppButton>
      </div>
    </div>
  </div>

  <!-- Loading -->
  <div v-else-if="pending" class="flex justify-center items-center py-40">
    <div class="w-8 h-8 border-2 border-white/10 border-t-accent rounded-full animate-spin" />
  </div>

  <!-- Erreur -->
  <div v-else class="flex flex-col items-center gap-4 py-40 text-muted text-sm">
    <span>Événement introuvable</span>
    <NuxtLink to="/events" class="text-primary hover:text-accent transition-colors text-xs">
      ← Retour au catalogue
    </NuxtLink>
  </div>

</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Heart, Share2 } from 'lucide-vue-next'
import { useWaitlist } from '~/composables/useWaitlist'
import { useBooking } from '~/composables/useBooking'
import { useEventsStore } from '~/stores/events'
import AppButton from '~/components/ui/AppButton.vue'
import type { ApiEvent } from '~/types/event'
import type { ApiBooking } from '~/types/booking'

definePageMeta({ layout: 'default' })

const route = useRoute()
const router = useRouter()
const { data: event, error , refresh  } = await useFetch<ApiEvent>(`/api/events/${route.params.id}`, {
  server: false,
  key: `event-detail-${route.params.id}`,
  watch: [() => route.params.id]
})

// Charger les ticket types de l'event
const { data: ticketTypes } = await useFetch<{ id_ticket_type: number; id_event: number; price: string; label: string; description: string; quantity: number }[]>(
  `/api/ticket_type_event/${route.params.id}`,
  { server: false, key: `ticket-types-${route.params.id}` }
)
const { createBooking } = useBooking()
const bookingLoading = ref(false)
const bookingError = ref<string | null>(null)
const { joinWaitlist, getPositionForEvent, loading: waitlistLoading, leaveWaitlist, getWaitlistEntryForEvent } = useWaitlist()

const qty = ref(1)
const isFollowing = ref(false)
const waitlistMessage = ref<string | null>(null)
const shareCopied = ref(false)

const eventsStore = useEventsStore()
eventsStore.loadLikes()

const isFavorite = computed(() => event.value ? eventsStore.isLiked(String(event.value.id_event)) : false)
const likesCount = computed(() => event.value?.like_count ?? 0)

// Données fictives en attendant l'API
const pending = ref(false)
const auth = useAuthStore()
// const availabilityPct = computed(() => {
//   if (!event.value) return 0
//   return Math.round((event.value.reserved / event.value.capacity) * 100)
// })

const isFull = computed(() => {
  if (!event.value) return false
  return event.value.reserved >= (event.value.capacity ?? 0)
})

const maxQty = computed(() => {
  if (!event.value) return 1
  return Math.min(10, (event.value.capacity ?? 0) - event.value.reserved)
})

const userWaitlistPosition = computed(() => {
  return getPositionForEvent(String(event.value?.id_event ?? ''))
})

// function formatDate(dateStr: string) {
//   return new Date(dateStr).toLocaleDateString('fr-FR', {
//     day: 'numeric', month: 'long', year: 'numeric',
//   })
// }

// Like / Unlike
async function toggleFavorite() {
  if (!auth.isAuthenticated) return navigateTo('/auth/login')
  if (!event.value) return
  const id = String(event.value.id_event)
  if (isFavorite.value) {
    await eventsStore.unlikeEvent(id)
  } else {
    await eventsStore.likeEvent(id)
  }
   await refresh()
}

// Partager
async function handleShare() {
  try {
    await navigator.clipboard.writeText(window.location.href)
    shareCopied.value = true
    setTimeout(() => { shareCopied.value = false }, 2000)
  } catch {
    shareCopied.value = false
  }
}

function toggleFollow() {
  if (!auth.isAuthenticated) return navigateTo('/auth/login')
  isFollowing.value = !isFollowing.value
}

async function handleReserve() {
  if (!auth.isAuthenticated) return navigateTo('/auth/login')
  if (!event.value) return

  bookingLoading.value = true
  bookingError.value = null
  try {
    const idTicketType = (
      ticketTypes.value?.find(t => t.label !== null && t.label !== '') ??
      ticketTypes.value?.[0]
    )?.id_ticket_type
    if (!idTicketType) {
      bookingError.value = 'Aucun type de billet disponible pour cet événement'
      return
    }
    await createBooking(event.value.id_event, qty.value, idTicketType)
    const constructed: ApiBooking = {
      id_event: event.value.id_event,
      id_ticket_type: idTicketType,
      quantity: qty.value,
      status_ticket: null,
    }
    useState<ApiBooking | null>('last-booking', () => null).value = constructed
    await router.push(`/booking/${event.value.id_event}`)
  } catch (err: any) {
    bookingError.value = err?.data?.detail ?? 'Erreur lors de la réservation'
  } finally {
    bookingLoading.value = false
  }
}

async function handleWaitlist() {
  if (!auth.isAuthenticated) return navigateTo('/auth/login')
  try {
    const entry = await joinWaitlist(String(event.value?.id_event ?? ''), qty.value)
    waitlistMessage.value = `Vous êtes en position ${entry.position} sur la liste d'attente`
    setTimeout(() => { waitlistMessage.value = null }, 5000)
  } catch (err) {
    waitlistMessage.value = ' Erreur lors de l\'ajout à la liste d\'attente'
    setTimeout(() => { waitlistMessage.value = null }, 5000)
  }
}
</script>