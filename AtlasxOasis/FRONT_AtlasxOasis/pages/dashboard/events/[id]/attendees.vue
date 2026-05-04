<template>
  <div class="min-h-screen bg-bg text-[#E9EEEC] flex flex-col">

    <!-- NAV -->
    <nav class="sticky top-0 z-50 flex items-center justify-between px-10 py-5 bg-bg/85 backdrop-blur-xl border-b border-white/5">
      <NuxtLink
        :to="`/dashboard/events`"
        class="font-title text-accent text-lg tracking-wide no-underline hover:text-primary transition-colors"
      >
        ← Mes événements
      </NuxtLink>
      <h1 class="font-title text-xl truncate max-w-md">
        {{ eventTitle || 'Participants' }}
      </h1>
      <button
        @click="exportCSV"
        class="px-4 py-2 rounded-lg bg-secondary/20 border border-secondary/30 text-[#E9EEEC] font-title text-[12px] hover:bg-secondary/30 transition-all flex items-center gap-2"
      >
        ⬇ Exporter CSV
      </button>
    </nav>

    <!-- CONTENT -->
    <section class="flex-1 px-10 py-8 flex flex-col gap-6">

      <!-- Stats -->
      <div class="grid grid-cols-3 gap-4">
        <div class="bg-s1 border border-white/5 rounded-xl p-5 text-center">
          <div class="font-title text-3xl text-accent">{{ eventReserved }}</div>
          <div class="text-xs text-muted mt-1 uppercase tracking-widest">Inscrits</div>
        </div>
        <div class="bg-s1 border border-white/5 rounded-xl p-5 text-center">
          <div class="font-title text-3xl text-green-400">{{ attendees.length }}</div>
          <div class="text-xs text-muted mt-1 uppercase tracking-widest">Détails disponibles</div>
        </div>
        <div class="bg-s1 border border-white/5 rounded-xl p-5 text-center">
          <div class="font-title text-3xl text-[#E9EEEC]/40">{{ eventCapacity ?? '—' }}</div>
          <div class="text-xs text-muted mt-1 uppercase tracking-widest">Capacité max</div>
        </div>
      </div>

      <!-- Search -->
      <div class="relative max-w-sm">
        <span class="absolute left-3 top-1/2 -translate-y-1/2 text-muted text-sm">🔍</span>
        <input
          v-model="search"
          type="text"
          placeholder="Rechercher par nom ou email…"
          class="w-full pl-9 pr-4 py-2.5 bg-s1 border border-white/10 rounded-lg text-sm text-[#E9EEEC] placeholder-muted focus:outline-none focus:border-accent/50 transition-colors"
        />
      </div>

      <!-- En attente endpoint -->
      <div v-if="!pending && attendees.length === 0" class="flex flex-col items-center justify-center py-16 bg-s1 border border-white/5 rounded-xl">
        <p class="text-muted text-sm">En attente de l'endpoint</p>
      </div>

      <!-- Table -->
      <div v-else class="overflow-x-auto border border-secondary/20 rounded-xl">
        <table class="w-full border-collapse">
          <thead>
            <tr class="bg-secondary/10 border-b border-secondary/20">
              <th class="px-6 py-4 text-left font-title text-[11px] font-semibold text-[#E9EEEC]/70 uppercase tracking-wider">Nom</th>
              <th class="px-6 py-4 text-left font-title text-[11px] font-semibold text-[#E9EEEC]/70 uppercase tracking-wider">Email</th>
              <th class="px-6 py-4 text-left font-title text-[11px] font-semibold text-[#E9EEEC]/70 uppercase tracking-wider">Billet</th>
              <th class="px-6 py-4 text-left font-title text-[11px] font-semibold text-[#E9EEEC]/70 uppercase tracking-wider">Date réservation</th>
              <th class="px-6 py-4 text-left font-title text-[11px] font-semibold text-[#E9EEEC]/70 uppercase tracking-wider">Statut</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="a in filteredAttendees"
              :key="a.id"
              class="border-b border-secondary/20 hover:bg-secondary/10 transition-colors"
            >
              <td class="px-6 py-4 font-body text-sm text-[#E9EEEC]">{{ a.name }}</td>
              <td class="px-6 py-4 font-body text-sm text-muted">{{ a.email }}</td>
              <td class="px-6 py-4 font-body text-sm text-[#E9EEEC]">{{ a.ticketType }}</td>
              <td class="px-6 py-4 font-body text-sm text-muted">{{ formatDate(a.bookingDate) }}</td>
              <td class="px-6 py-4">
                <span :class="statusClass(a.status)">
                  {{ statusLabel(a.status) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- No results after search -->
        <div v-if="filteredAttendees.length === 0" class="text-center py-8 text-muted text-sm">
          Aucun résultat pour « {{ search }} »
        </div>
      </div>

    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '~/stores/auth'

definePageMeta({ layout: false })

const route = useRoute()
const authStore = useAuthStore()
const eventId = route.params.id as string

// ── Types ──────────────────────────────────────────────────
interface Attendee {
  id: string
  name: string
  email: string
  ticketType: string
  bookingDate: string
  status: string
}

// ── Fetch event (titre + reserved + capacity) ──────────────
const eventTitle = ref('')
const eventReserved = ref(0)
const eventCapacity = ref<number | null>(null)
const { data: eventData } = await useAsyncData(`event-${eventId}`, () =>
  $fetch<any>(`/api/events/${eventId}`),
  { server: false }
)
watch(eventData, (v) => {
  if (v) {
    eventTitle.value = v.title ?? v.name ?? `Événement #${eventId}`
    eventReserved.value = v.reserved ?? 0
    eventCapacity.value = v.capacity ?? v.max_capacity ?? null
  }
}, { immediate: true })

// ── Fetch participants (endpoint dédié si disponible) ───────
const pending = ref(false)
const fetchError = ref<string | null>(null)
const attendees = ref<Attendee[]>([])

onMounted(async () => {
  pending.value = true
  try {
    const raw = await $fetch<any[]>(`/api/bookings/event/${eventId}`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    attendees.value = (raw ?? []).map((item: any) => ({
      id: String(item.id_sale_object ?? item.id_booking ?? item.id_customer ?? Math.random()),
      name: item.user_name ?? item.name ?? item.username ?? `Participant #${item.id_customer ?? '?'}`,
      email: item.user_email ?? item.email ?? '—',
      ticketType: item.label ?? item.ticket_type ?? item.ticket_label ?? 'Standard',
      bookingDate: item.date_payment ?? item.created_at ?? item.booking_date ?? '',
      status: (item.status_status ?? item.status_ticket ?? item.status ?? 'confirmed').toLowerCase(),
    }))
  } catch {
    // Endpoint non disponible — la liste reste vide, le count vient de eventReserved
  } finally {
    pending.value = false
  }
})

// ── Search ──────────────────────────────────────────────────
const search = ref('')

const filteredAttendees = computed(() => {
  const q = search.value.toLowerCase().trim()
  if (!q) return attendees.value
  return attendees.value.filter(a =>
    a.name.toLowerCase().includes(q) || a.email.toLowerCase().includes(q)
  )
})

// ── Stats ───────────────────────────────────────────────────

// ── Helpers ─────────────────────────────────────────────────
function formatDate(d: string) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}

function statusLabel(s: string) {
  const map: Record<string, string> = {
    confirmed: 'Confirmé',
    pending:   'En attente',
    cancelled: 'Annulé',
    waitlist:  'Liste attente',
  }
  return map[s] ?? s
}

function statusClass(s: string) {
  const base = 'px-3 py-1 rounded-full text-[10px] font-semibold uppercase tracking-wider '
  const map: Record<string, string> = {
    confirmed: base + 'bg-green-500/20 text-green-400',
    pending:   base + 'bg-yellow-500/20 text-yellow-400',
    cancelled: base + 'bg-red-500/20 text-red-400',
    waitlist:  base + 'bg-blue-500/20 text-blue-400',
  }
  return map[s] ?? base + 'bg-gray-500/20 text-gray-400'
}

// ── Export CSV ───────────────────────────────────────────────
function exportCSV() {
  const rows = [
    ['Nom', 'Email', 'Type de billet', 'Date de réservation', 'Statut'],
    ...filteredAttendees.value.map(a => [
      a.name,
      a.email,
      a.ticketType,
      formatDate(a.bookingDate),
      statusLabel(a.status),
    ]),
  ]
  const csv = rows.map(r => r.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(',')).join('\n')
  const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `participants-${eventId}.csv`
  a.click()
  URL.revokeObjectURL(url)
}
</script>

