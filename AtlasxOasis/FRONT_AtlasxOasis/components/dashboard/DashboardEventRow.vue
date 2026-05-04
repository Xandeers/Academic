<template>
  <tr class="border-b border-secondary/20 hover:bg-secondary/10 transition-colors">
    <!-- Titre -->
    <td class="px-6 py-4 font-body text-sm text-[#E9EEEC]">{{ event.title }}</td>

    <!-- Date -->
    <td class="px-6 py-4 font-body text-sm text-muted">{{ formatDate(event.date) }}</td>

    <!-- Statut -->
    <td class="px-6 py-4">
      <span :class="['px-3 py-1 rounded-full text-[10px] font-semibold uppercase tracking-wider', statusClass]">
        {{ event.status }}
      </span>
    </td>

    <!-- Participants -->
    <td class="px-6 py-4 font-body text-sm text-[#E9EEEC]">{{ event.participants }} inscrits</td>

    <!-- Actions -->
    <td class="px-6 py-4 flex items-center gap-3">
      <NuxtLink
        :to="`/dashboard/events/${event.id}/attendees`"
        class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-secondary/30 text-[11px] font-semibold text-[#E9EEEC]/70 hover:bg-secondary/10 transition-colors no-underline"
      >
        <Users :size="14" />
        Participants
      </NuxtLink>
      <button
        @click="$emit('edit', event)"
        class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-accent/30 text-[11px] font-semibold text-accent hover:bg-accent/10 transition-colors"
      >
        <Edit :size="14" />
        Modifier
      </button>
      <button
        @click="$emit('delete', event)"
        class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-red-500/30 text-[11px] font-semibold text-red-400 hover:bg-red-500/10 transition-colors"
      >
        <Trash2 :size="14" />
        Supprimer
      </button>
    </td>
  </tr>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Edit, Trash2, Users } from 'lucide-vue-next'

interface Event {
  id: string
  title: string
  date: string
  status: 'Brouillon' | 'Publié' | 'Archivé' | 'Annulé'
  participants: number
}

const props = defineProps<{ event: Event }>()
defineEmits(['edit', 'delete'])

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}

const statusClass = computed(() => {
  const status = props.event.status
  const classes: Record<string, string> = {
    'Brouillon': 'bg-gray-500/20 text-gray-300',
    'Publié': 'bg-green-500/20 text-green-400',
    'Archivé': 'bg-blue-500/20 text-blue-400',
    'Annulé': 'bg-red-500/20 text-red-400',
  }
  return classes[status] || 'bg-gray-500/20 text-gray-300'
})
</script>
