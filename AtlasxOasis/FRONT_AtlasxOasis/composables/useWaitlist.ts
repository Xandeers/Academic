import { ref, computed } from 'vue'
import type { Ticket } from '~/types/booking'

export interface WaitlistEntry {
    id: string
    userId: string
    eventId: string
    position: number
    joinedAt: string
    status: 'waiting' | 'notified' | 'expired'
    ticketsRequested: number
}

export const useWaitlist = () => {
    const waitlist = ref<WaitlistEntry[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)

    // Charger les entrées de liste d'attente depuis sessionStorage
    const loadFromStorage = () => {
        if (typeof window !== 'undefined') {
            const stored = sessionStorage.getItem('mock_waitlist')
            if (stored) {
                try {
                    waitlist.value = JSON.parse(stored)
                } catch (e) {
                    waitlist.value = []
                }
            }
        }
    }

    // Sauvegarder dans sessionStorage
    const saveToStorage = () => {
        if (typeof window !== 'undefined') {
            sessionStorage.setItem('mock_waitlist', JSON.stringify(waitlist.value))
        }
    }

    // Ajouter à la liste d'attente
    const joinWaitlist = async (eventId: string, ticketsRequested: number = 1): Promise<WaitlistEntry> => {
        loading.value = true
        error.value = null
        try {
            // TODO: Appel API /api/waitlist (POST)
            // const entry = await $fetch('/api/waitlist', {
            //   method: 'POST',
            //   body: { eventId, ticketsRequested }
            // })

            // Position = nombre d'entrées existantes + 1
            const position = waitlist.value.filter(w => w.id.includes(eventId)).length + 1

            const newEntry: WaitlistEntry = {
                id: `waitlist_${Date.now()}`,
                userId: '', // Récupéré du store auth
                eventId: eventId,
                position: position,
                joinedAt: new Date().toISOString(),
                status: 'waiting',
                ticketsRequested: ticketsRequested
            }

            waitlist.value.push(newEntry)
            saveToStorage()
            return newEntry
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Erreur lors de l\'ajout à la liste d\'attente'
            error.value = message
            throw err
        } finally {
            loading.value = false
        }
    }

    // Quitter la liste d'attente
    const leaveWaitlist = async (waitlistId: string): Promise<void> => {
        loading.value = true
        error.value = null
        try {
            // TODO: Appel API /api/waitlist/{id} (DELETE)
            // await $fetch(`/api/waitlist/${waitlistId}`, { method: 'DELETE' })

            const index = waitlist.value.findIndex(w => w.id === waitlistId)
            if (index > -1) {
                waitlist.value.splice(index, 1)
                saveToStorage()
            }
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Erreur lors du retrait de la liste d\'attente'
            error.value = message
            throw err
        } finally {
            loading.value = false
        }
    }

    // Récupérer les entrées d'un utilisateur
    const getUserWaitlistEntries = computed(() => {
        return waitlist.value
    })

    // Récupérer la position pour un événement spécifique
    const getPositionForEvent = (eventId: string): number | null => {
        const entry = waitlist.value.find(w => w.eventId === eventId && w.status === 'waiting')
        return entry ? entry.position : null
    }

    // Récupérer l'entrée waitlist pour un événement
    const getWaitlistEntryForEvent = (eventId: string): WaitlistEntry | null => {
        return waitlist.value.find(w => w.eventId === eventId && w.status === 'waiting') || null
    }

    // Notifier un utilisateur (quand une place se libère)
    const notifyUser = (waitlistId: string): void => {
        const entry = waitlist.value.find(w => w.id === waitlistId)
        if (entry) {
            entry.status = 'notified'
            saveToStorage()

            // Afficher une notification
            if (typeof window !== 'undefined' && 'Notification' in window) {
                new Notification('AtlasXOasis', {
                    body: 'Une place est disponible pour l\'événement. Réservez rapidement!'
                })
            }
        }
    }

    // Initialiser au premier appel
    loadFromStorage()

    return {
        waitlist,
        loading,
        error,
        joinWaitlist,
        leaveWaitlist,
        getUserWaitlistEntries,
        getPositionForEvent,
        getWaitlistEntryForEvent,
        notifyUser
    }
}
