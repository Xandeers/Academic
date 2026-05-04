<template>
  <div class="min-h-screen bg-bg text-[#E9EEEC] flex flex-col">
    <!-- NAV -->
    <nav class="sticky top-0 z-50 flex items-center justify-between px-10 py-5 bg-bg/85 backdrop-blur-xl border-b border-white/5">
      <NuxtLink to="/dashboard" class="font-title text-accent text-lg tracking-wide no-underline hover:text-primary transition-colors">
        ← Dashboard
      </NuxtLink>
      <h1 class="font-title text-xl">Mes événements</h1>
      <NuxtLink
        to="/dashboard/events/create"
        class="px-4 py-2 rounded-lg bg-accent text-[#0b2618] font-title text-[12px] hover:shadow-[0_0_20px_rgba(56,227,143,0.35)] transition-all no-underline"
      >
        + Créer un événement
      </NuxtLink>
    </nav>

    <!-- TABLE -->
    <section class="flex-1 px-10 py-8">
      <div v-if="pending" class="flex justify-center py-12">
        <span class="text-muted">Chargement…</span>
      </div>

      <template v-else>
        <div class="overflow-x-auto border border-secondary/20 rounded-xl">
          <table class="w-full border-collapse">
            <thead>
              <tr class="bg-secondary/10 border-b border-secondary/20">
                <th class="px-6 py-4 text-left font-title text-[11px] font-semibold text-[#E9EEEC]/70 uppercase tracking-wider">Titre</th>
                <th class="px-6 py-4 text-left font-title text-[11px] font-semibold text-[#E9EEEC]/70 uppercase tracking-wider">Date</th>
                <th class="px-6 py-4 text-left font-title text-[11px] font-semibold text-[#E9EEEC]/70 uppercase tracking-wider">Statut</th>
                <th class="px-6 py-4 text-left font-title text-[11px] font-semibold text-[#E9EEEC]/70 uppercase tracking-wider">Participants</th>
                <th class="px-6 py-4 text-left font-title text-[11px] font-semibold text-[#E9EEEC]/70 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody>
              <DashboardEventRow
                v-for="event in events"
                :key="event.id"
                :event="event"
                @edit="handleEdit"
                @delete="handleDelete"
              />
            </tbody>
          </table>
        </div>

        <!-- Pas d'événements -->
        <div v-if="events.length === 0" class="flex flex-col items-center justify-center py-12">
          <div class="text-muted mb-4">📭</div>
          <p class="font-title text-lg text-[#E9EEEC]/70">Aucun événement créé</p>
          <NuxtLink
            to="/dashboard/events/create"
            class="mt-4 px-4 py-2 rounded-lg bg-accent text-[#0b2618] font-title text-[12px] hover:shadow-[0_0_20px_rgba(56,227,143,0.35)] transition-all no-underline"
          >
            Créer votre premier événement
          </NuxtLink>
        </div>
      </template>
    </section>

    <!-- Modal de confirmation de suppression -->
    <AppModal
      v-model="showDeleteModal"
      title="Supprimer l'événement"
      confirmLabel="Supprimer"
      cancelLabel="Annuler"
      :loading="isDeleting"
      @confirm="confirmDelete"
    >
      <p class="font-body text-sm text-[#E9EEEC]/80">
        Êtes-vous sûr de vouloir supprimer
        <span class="font-semibold text-[#E9EEEC]">{{ eventToDelete?.title }}</span> ?
        Cette action est irréversible.
      </p>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '~/stores/auth'

definePageMeta({ layout: false })

const authStore = useAuthStore()

interface Event {
  id: string
  title: string
  date: string
  status: 'Brouillon' | 'Publié' | 'Archivé' | 'Annulé'
  participants: number
}

const statusMap: Record<string, Event['status']> = {
  published: 'Publié',
  draft: 'Brouillon',
  archived: 'Archivé',
  cancelled: 'Annulé',
}

const { data: rawEvents, pending } = await useAsyncData('dashboard-my-events', () =>
  $fetch<any[]>('/api/events/'),
  { server: false }
)

const events = computed<Event[]>(() =>
  (rawEvents.value ?? []).map((e: any) => ({
    id: String(e.id_event),
    title: e.title ?? e.name ?? '(sans titre)',
    date: e.begin_date ?? e.start_date,
    status: statusMap[e.status ?? e.event_status] ?? 'Brouillon',
    participants: e.reserved ?? 0,
  }))
)

// — État modal suppression —
const showDeleteModal = ref(false)
const eventToDelete = ref<Event | null>(null)
const isDeleting = ref(false)

function handleEdit(event: Event) {
  navigateTo(`/dashboard/events/${event.id}/edit`)
}

function handleDelete(event: Event) {
  eventToDelete.value = event
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (!eventToDelete.value) return
  isDeleting.value = true
  try {
    await $fetch(`/api/events/${eventToDelete.value.id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    await refreshNuxtData('dashboard-my-events')
    showDeleteModal.value = false
    eventToDelete.value = null
  } catch (err) {
    console.error('Erreur lors de la suppression:', err)
  } finally {
    isDeleting.value = false
  }
}
</script>
