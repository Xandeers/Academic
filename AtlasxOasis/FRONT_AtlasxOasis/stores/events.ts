import { defineStore } from 'pinia'
import type { ApiEvent, EventCategory } from '~/types/event'

export const useEventsStore = defineStore('events', {
  state: () => ({
    events: [] as ApiEvent[],
    activeFilter: 'Tout' as EventCategory | 'Tout',
    searchQuery: '',
    isLoading: false,
    error: null as string | null,
    // IDs des événements likés par l'utilisateur (persisté localStorage)
    likedEventIds: [] as string[],
  }),
  getters: {
    filteredEvents(state) {
      let list = state.events
      if (state.activeFilter !== 'Tout')
        list = list.filter(e => e.category[0]?.name === state.activeFilter || e.category[0]?.label === state.activeFilter)
      if (state.searchQuery.trim()) {
        const q = state.searchQuery.toLowerCase()
        list = list.filter(e =>
          e.title.toLowerCase().includes(q)
        )
      }
      return list
    },
    likedEvents(state): ApiEvent[] {
      return state.events.filter(e => state.likedEventIds.includes(String(e.id_event)))
    },
    isLiked: (state) => (eventId: string) => state.likedEventIds.includes(String(eventId)),
  },
  actions: {
    async fetchEvents() {
      this.isLoading = true; this.error = null
      try {
        this.events = await $fetch<ApiEvent[]>('/api/events/')
      } catch { this.error = 'Impossible de charger les événements' }
      finally { this.isLoading = false }
    },
    setFilter(f: EventCategory | 'Tout') { this.activeFilter = f },
    setSearch(q: string) { this.searchQuery = q },

    // Charger les likes depuis localStorage
    loadLikes() {
      if (import.meta.client) {
        const stored = localStorage.getItem('liked_events')
        if (stored) {
          try { this.likedEventIds = JSON.parse(stored) } catch { this.likedEventIds = [] }
        }
      }
    },
    // Sauvegarder dans localStorage
    saveLikes() {
      if (import.meta.client) {
        localStorage.setItem('liked_events', JSON.stringify(this.likedEventIds))
      }
    },
    async likeEvent(eventId: string) {
      if (this.likedEventIds.includes(eventId)) return
      this.likedEventIds.push(eventId)
      this.saveLikes()
      // Pas d'endpoint like dans l'API — persistance localStorage uniquement
    },
    async unlikeEvent(eventId: string) {
      this.likedEventIds = this.likedEventIds.filter(id => id !== eventId)
      this.saveLikes()
      // Pas d'endpoint unlike dans l'API — persistance localStorage uniquement
    },
  },
})