<template>
 <div class="min-h-screen bg-bg px-5 py-10">
    <div class="max-w-5xl mx-auto">

      <!-- Header -->
      <div class="mb-12">
        <h1 class="font-title text-4xl text-[#E9EEEC] uppercase tracking-wide mb-2">
          Mon Profil
        </h1>
        <p class="text-muted">Gérez vos informations et vos billets</p>
      </div>

      <!-- Profil Section -->
      <div class="mb-12 bg-s1 border border-white/5 rounded-2xl p-8">
        <div class="flex items-center gap-6 mb-8 max-md:flex-col">
          <div class="w-16 h-16 rounded-full bg-secondary/30 border border-secondary/40 flex items-center justify-center font-title text-2xl text-accent flex-shrink-0">
            {{ initials }}
          </div>
          <div>
            <h2 class="font-title text-xl text-[#E9EEEC]">{{ auth.fullName }}</h2>
            <p class="text-xs text-muted mt-1">{{ auth.user?.email }}</p>
            <span class="inline-flex items-center gap-1.5 mt-2 text-[10px] font-title tracking-widest text-accent bg-accent/10 border border-accent/20 rounded-full px-3 py-1">
              {{ auth.user?.role === 'organizer' ? 'Organisateur' : 'Participant' }}
            </span>
          </div>
          <AppButton variant="ghost" class="ml-auto" @click="editMode = !editMode">
            {{ editMode ? 'Annuler' : 'Modifier' }}
          </AppButton>
        </div>

        <!-- Formulaire modification -->
      <div v-if="editMode" class="flex flex-col gap-4">
       <AppInput v-model="form.username" label="Pseudo" placeholder="monpseudo" />
       <AppInput v-model="form.email" label="Email" placeholder="vous@email.com" type="email" />
       <AppButton variant="primary" class="w-fit" :loading="loadingSave" @click="saveProfile">
          Enregistrer
       </AppButton>
      </div>

        <!-- Infos affichage -->
      <div v-else class="grid grid-cols-2 gap-4">
  <div class="bg-s2 rounded-lg p-4 col-span-2">
    <div class="text-[10px] text-muted font-title tracking-widest uppercase mb-1">Pseudo</div>
    <div class="text-sm text-[#E9EEEC]">{{ auth.user?.username }}</div>
  </div>
  <div class="bg-s2 rounded-lg p-4 col-span-2">
    <div class="text-[10px] text-muted font-title tracking-widest uppercase mb-1">Email</div>
    <div class="text-sm text-[#E9EEEC]">{{ auth.user?.email }}</div>
  </div>
</div>
</div>
      <!-- Profils suivis -->
      <div>
        <h2 class="font-title text-4xl text-[#E9EEEC] uppercase tracking-wide mb-6">
          Profils suivis
        </h2>
        <div class="overflow-x-hidden overflow-y-auto h-96">
          <div 
            v-for="profile in followedProfiles"
            class="p-6 mb-6 bg-s1 border border-white/5 rounded-2xl flex flex-row justify-between"
          >
            <div class="flex flex-row">
              <div class="w-16 h-16 rounded-full bg-secondary/30 border border-secondary/40 flex items-center justify-center font-title text-2xl text-accent flex-shrink-0 mx-2">
              </div>
              <div class="flex flex-col justify-center mx-2">
                <div class="text-sm font-semibold text-[#E9EEEC] hover:underline hover:cursor-pointer">
                  {{ profile.followed_user.username }}
                </div>
                <div class="text-xs text-muted">
                  {{ profile.followed_user.type_user }}
                </div>
              </div>
            </div>
            <div class="flex flex-col justify-center">
              <AppButton class="max-md:text-[8px]" variant="danger" @click="unfollow(profile.followed_user.id_user)">
                Ne plus suivre
              </AppButton>
            </div>
          </div>
        </div>
      </div>

      <!-- Mes Billets Section -->
      <div class="mb-12">
        <div class="mb-8">
          <h2 class="font-title text-2xl text-[#E9EEEC] uppercase tracking-wide mb-6">
            Mes Billets
          </h2>
          <div class="flex gap-3 mb-8 border-b border-accent/10">
            <button
              @click="filterStatus = 'all'"
              :class="[
                'px-4 py-2 text-sm font-semibold uppercase tracking-wide transition-colors',
                filterStatus === 'all' ? 'text-accent border-b-2 border-accent' : 'text-muted hover:text-[#E9EEEC]'
              ]"
            >Tous les billets</button>
            <button
              @click="filterStatus = 'active'"
              :class="[
                'px-4 py-2 text-sm font-semibold uppercase tracking-wide transition-colors',
                filterStatus === 'active' ? 'text-accent border-b-2 border-accent' : 'text-muted hover:text-[#E9EEEC]'
              ]"
            >Actifs</button>
            <button
              @click="filterStatus = 'past'"
              :class="[
                'px-4 py-2 text-sm font-semibold uppercase tracking-wide transition-colors',
                filterStatus === 'past' ? 'text-accent border-b-2 border-accent' : 'text-muted hover:text-[#E9EEEC]'
              ]"
            >Passés</button>
          </div>
        </div>

        <div v-if="loadingTickets" class="text-center py-12 px-5">
          <div class="w-10 h-10 mx-auto mb-5 border-4 border-accent/20 border-t-accent rounded-full animate-spin" />
          <p class="text-muted">Chargement de vos billets...</p>
        </div>

        <div v-else-if="filteredTickets.length > 0" class="grid grid-cols-1 gap-8">
          <div v-for="ticket in filteredTickets" :key="ticket.id" class="relative">
            <BookingTicket :ticket="ticket" :showActions="false" />
            <div class="mt-4 flex gap-3 justify-center">
              <AppButton
                v-if="isTicketActive(ticket)"
                variant="ghost"
                @click="openCancelModal(ticket)"
                :loading="loadingCancel === ticket.id"
              >Se désister</AppButton>
              <AppButton v-else variant="ghost" disabled>
                Événement passé
              </AppButton>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-12 px-5">
          <div class="text-5xl mb-4">🎫</div>
          <h3 class="font-title text-xl text-[#E9EEEC] mb-2">Aucun billet</h3>
          <p class="text-muted mb-6">
            {{
              filterStatus === 'active'
                ? 'Vous n\'avez aucun billet actif pour le moment.'
                : filterStatus === 'past'
                ? 'Vous n\'avez pas d\'événement passé.'
                : 'Vous n\'avez pas de billets. Réservez maintenant!'
            }}
          </p>
          <AppButton variant="primary" @click="goToEvents">
            Explorer les événements
          </AppButton>
        </div>
      </div>

      <!-- Mes Favoris Section -->
      <div class="mb-12">
        <h2 class="font-title text-2xl text-[#E9EEEC] uppercase tracking-wide mb-6">
          Mes Favoris
        </h2>

        <div v-if="loadingFavorites" class="text-center py-12">
          <div class="w-10 h-10 mx-auto mb-5 border-4 border-accent/20 border-t-accent rounded-full animate-spin" />
          <p class="text-muted">Chargement...</p>
        </div>

        <div v-else-if="favoriteEvents.length > 0" class="grid grid-cols-1 gap-4">
          <div
            v-for="event in favoriteEvents"
            :key="event.id"
            class="bg-s1 border border-white/5 rounded-2xl p-6 flex items-center justify-between gap-4"
          >
            <div class="flex flex-col gap-1 min-w-0">
              <NuxtLink
                :to="`/events/${event.id}`"
                class="font-title text-base text-[#E9EEEC] hover:text-accent transition-colors no-underline truncate"
              >
                {{ event.title }}
              </NuxtLink>
              <p class="text-xs text-muted">
                {{ event.date ? new Date(event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : '—' }}
                <span v-if="event.location"> · {{ event.location }}</span>
              </p>
              <span class="text-xs text-accent font-semibold">
                {{ event.price === 0 ? 'Gratuit' : `${event.price} €` }}
              </span>
            </div>
            <AppButton
              variant="ghost"
              :loading="unlikingId === event.id"
              @click="removeFavorite(event.id)"
            >
              ♥ Retirer
            </AppButton>
          </div>
        </div>

        <div v-else class="text-center py-12 px-5">
          <div class="text-5xl mb-4">♡</div>
          <h3 class="font-title text-xl text-[#E9EEEC] mb-2">Aucun favori</h3>
          <p class="text-muted mb-6">Likez des événements pour les retrouver ici.</p>
          <AppButton variant="primary" @click="goToEvents">Explorer les événements</AppButton>
        </div>
      </div>

      <!-- Ma Liste d'attente Section -->
      <div class="mb-12">
        <h2 class="font-title text-2xl text-[#E9EEEC] uppercase tracking-wide mb-6">
          Ma Liste d'Attente
        </h2>

        <div v-if="loadingWaitlist" class="text-center py-12 px-5">
          <div class="w-10 h-10 mx-auto mb-5 border-4 border-accent/20 border-t-accent rounded-full animate-spin" />
          <p class="text-muted">Chargement...</p>
        </div>

        <div v-else-if="userWaitlistEntries.length > 0" class="grid grid-cols-1 gap-4">
          <div
            v-for="entry in userWaitlistEntries"
            :key="entry.id"
            class="bg-gradient-to-br from-s1 to-s2 border border-accent/10 rounded-xl p-6"
          >
            <div class="flex items-center justify-between mb-4">
              <div>
                <h3 class="font-title text-lg text-[#E9EEEC] mb-2">Position #{{ entry.position }}</h3>
                <p class="text-sm text-muted">
                  {{ entry.ticketsRequested }} place{{ entry.ticketsRequested > 1 ? 's' : '' }} demandée{{ entry.ticketsRequested > 1 ? 's' : '' }}
                </p>
              </div>
              <div :class="[
                'px-4 py-2 rounded-lg font-semibold text-sm',
                entry.status === 'waiting' ? 'bg-yellow-500/10 text-yellow-400' :
                entry.status === 'notified' ? 'bg-green-500/10 text-green-400' :
                'bg-red-500/10 text-red-400'
              ]">
                {{ entry.status === 'waiting' ? 'En attente' : entry.status === 'notified' ? 'Notifié' : 'Expiré' }}
              </div>
            </div>
            <p class="text-xs text-muted mb-4">
              Inscrit le {{ new Date(entry.joinedAt).toLocaleDateString('fr-FR') }}
            </p>
            <AppButton
              variant="ghost"
              class="w-full justify-center"
              @click="cancelWaitlist(entry)"
              :loading="loadingCancelWaitlist === entry.id"
            >Quitter la liste</AppButton>
          </div>
        </div>

        <div v-else class="text-center py-12 px-5">
          <div class="text-5xl mb-4">⏳</div>
          <h3 class="font-title text-xl text-[#E9EEEC] mb-2">Pas en liste d'attente</h3>
          <p class="text-muted mb-6">Vous n'êtes inscrit à aucune liste d'attente pour le moment.</p>
          <AppButton variant="primary" @click="goToEvents">
            Parcourir les événements
          </AppButton>
        </div>
      </div>

      <!-- Modal Confirmation Annulation -->
      <AppModal
        v-model="showCancelModal"
        title="Confirmer l'annulation"
        confirmLabel="Annuler ma reservaton"
        cancelLabel="Garder ma reservation"
        :loading="loadingCancel !== null"
        @confirm="confirmCancelTicket"
      >
        <div>
          <p class="mb-4">
            Êtes-vous sûr de vouloir annuler votre billet pour ?
          </p>
          <p class="text-[#99D7B8] font-semibold mb-4" v-if="ticketToCancel">
            {{ ticketToCancel.eventTitle }} — {{ new Date(ticketToCancel.eventDate).toLocaleDateString('fr-FR') }}
          </p>
          <p class="text-sm text-muted">
            Cette action est irréversible. Vous ne pourrez pas accéder à cet événement avec ce billet.
          </p>
        </div>
      </AppModal>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import type { Ticket } from '~/types/booking'
import type { WaitlistEntry } from '~/composables/useWaitlist'
import { useBooking } from '~/composables/useBooking'
import { useAuthStore } from '~/stores/auth'
import { useEventsStore } from '~/stores/events'
import BookingTicket from '~/components/booking/BookingTicket.vue'
import AppButton from '~/components/ui/AppButton.vue'
import AppInput from '~/components/ui/AppInput.vue'
import AppModal from '~/components/ui/AppModal.vue'

definePageMeta({ layout: 'default', middleware: 'auth' })

const router = useRouter()
const auth = useAuthStore()
const { cancelBooking, fetchBookings } = useBooking()
const { leaveWaitlist, waitlist: waitlistEntries } = useWaitlist()

// --- Profil ---
const editMode = ref(false)
const loadingSave = ref(false)

const initials = computed(() => {
  if (!auth.user) return '?'
  return auth.user.username.slice(0, 2).toUpperCase()
})

const form = reactive({
  username: auth.user?.username ?? '',
  email: auth.user?.email ?? '',
})
watch(() => auth.user, (user) => {
  if (user) {
    form.username = user.username
    form.email = user.email
  }
}, { immediate: true })
async function saveProfile() {
  loadingSave.value = true
  try {

  await $fetch('/api/customers/', {
      method: 'PUT',
      body: {
        firstname: '',
        lastname: '',
        username: form.username,
        description: auth.user?.description ?? '',
      },
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    if (auth.user) {
      auth.user.username = form.username
    }
    editMode.value = false
  } catch (e: any) {
    console.error('Erreur sauvegarde:', e)
  } finally {
    loadingSave.value = false
  }

}

// --- Billets ---
const filterStatus = ref<'all' | 'active' | 'past'>('all')
const loadingTickets = ref(false)
const loadingCancel = ref<string | null>(null)
const allTickets = ref<Ticket[]>([])
const showCancelModal = ref(false)
const ticketToCancel = ref<Ticket | null>(null)

const loadTickets = async () => {
  loadingTickets.value = true
  try {
    if (eventsStore.events.length === 0) await eventsStore.fetchEvents()
    const bookings = await fetchBookings()
    const eventsMap = new Map(eventsStore.events.map((e: any) => [e.id_event, e]))
    allTickets.value = bookings.map((b: any) => {
      const ev = eventsMap.get(b.id_event) as any
      return {
        id: `${b.id_event}-${b.id_ticket_type}`,
        bookingId: String(b.id_event),
        idTicketType: b.id_ticket_type,
        eventId: String(b.id_event),
        eventTitle: ev?.title ?? `Événement #${b.id_event}`,
        eventDate: ev?.begin_date ?? '',
        eventTime: ev?.begin_date ? new Date(ev.begin_date).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }) : '',
        eventLocation: '',
        eventCategory: ev?.category?.[0]?.name ?? ev?.category?.[0]?.label ?? '',
        holderName: auth.user?.username ?? '',
        ticketNumber: `ATX${String(b.id_event).padStart(8, '0')}`,
        ticketType: 'Standard',
        qrCodeData: `booking:event:${b.id_event}:ticket:${b.id_ticket_type}`,
        price: (ev?.price ?? 0) * (b.quantity ?? 1),
      }
    })
  } catch (e) {
    console.error('Erreur chargement billets:', e)
  } finally {
    loadingTickets.value = false
  }
}

const isTicketActive = (ticket: Ticket): boolean =>
  new Date(ticket.eventDate) > new Date()

const filteredTickets = computed(() => {
  if (filterStatus.value === 'active') return allTickets.value.filter(t => isTicketActive(t))
  if (filterStatus.value === 'past') return allTickets.value.filter(t => !isTicketActive(t))
  return allTickets.value
})

const openCancelModal = (ticket: Ticket) => {
  ticketToCancel.value = ticket
  showCancelModal.value = true
}

const confirmCancelTicket = async () => {
  if (!ticketToCancel.value) return
  loadingCancel.value = ticketToCancel.value.id
  try {
    await cancelBooking(ticketToCancel.value.eventId, ticketToCancel.value.idTicketType ?? 1, 1)
    allTickets.value = allTickets.value.filter(t => t.id !== ticketToCancel.value!.id)
    showCancelModal.value = false
    ticketToCancel.value = null
  } catch (e) {
    console.error('Erreur annulation:', e)
  } finally {
    loadingCancel.value = null
  }
}

// --- Liste d'attente ---
const loadingWaitlist = ref(false)
const loadingCancelWaitlist = ref<string | null>(null)
const userWaitlistEntries = ref<WaitlistEntry[]>([])

const loadWaitlist = () => {
  userWaitlistEntries.value = waitlistEntries.value
}

const cancelWaitlist = async (entry: WaitlistEntry) => {
  loadingCancelWaitlist.value = entry.id
  try {
    await leaveWaitlist(entry.id)
    userWaitlistEntries.value = userWaitlistEntries.value.filter(e => e.id !== entry.id)
  } catch (error) {
    console.error('Erreur retrait liste attente:', error)
  } finally {
    loadingCancelWaitlist.value = null
  }
}

// --- Favoris ---
interface FavoriteEvent {
  id: string
  title: string
  date: string
  location: string
  price: number
}

const eventsStore = useEventsStore()
const loadingFavorites = ref(false)
const unlikingId = ref<string | null>(null)

const favoriteEvents = computed<FavoriteEvent[]>(() =>
  eventsStore.likedEvents.map((e: any) => ({
    id: String(e.id_event ?? e.id),
    title: e.title ?? '',
    date: e.begin_date ?? e.date ?? '',
    location: e.location_id?.[0] ? `Lieu #${e.location_id[0]}` : '',
    price: e.price ?? 0,
  }))
)

const loadFavorites = async () => {
  loadingFavorites.value = true
  eventsStore.loadLikes()
  if (eventsStore.events.length === 0) await eventsStore.fetchEvents()
  loadingFavorites.value = false
}

const removeFavorite = async (eventId: string) => {
  unlikingId.value = eventId
  await eventsStore.unlikeEvent(eventId)
  unlikingId.value = null
}

// --- Navigation ---
const goToEvents = () => router.push('/events')

onMounted(() => {
  loadTickets()
  loadWaitlist()
  loadFavorites()
})

// Données fictives pour tester "Profils Suivis" en attendant l'API
// Il faudra aussi ajouter la possibilité d'unfollow depuis cette page
const { data: followedProfiles, refresh } = await useFetch(`/api/users/${auth.user.id}/followed`)

async function unfollow(id) {
  await $fetch(`/api/users/${id}/unfollow`, { 
    method: 'DELETE', 
    headers: { Authorization: `Bearer ${auth.token}` } 
  })
  await refresh()
}
</script>