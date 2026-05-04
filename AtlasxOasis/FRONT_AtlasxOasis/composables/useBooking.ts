import { ref } from 'vue'
import type { ApiBooking } from '~/types/booking'

export const useBooking = () => {
    const auth = useAuthStore()
    const loading = ref(false)
    const error = ref<string | null>(null)

    /** GET /api/bookings/my-bookings — liste des réservations de l'utilisateur connecté */
    const fetchBookings = async (): Promise<ApiBooking[]> => {
        loading.value = true
        error.value = null
        try {
            return await $fetch<ApiBooking[]>('/api/bookings/my_bookings', {
                headers: { Authorization: `Bearer ${auth.token}`,
                               'Accept': 'application/json',
  },
            })
        } catch {
            error.value = 'Impossible de charger les réservations'
            return []
        } finally {
            loading.value = false
        }
    }

    /** POST /api/bookings/{event_id} — créer une réservation
     *  Body: { id_ticket_type: number, quantity: number }
     *  id_ticket_type est requis par l'API (défaut: 1 si inconnu)
     */
    const createBooking = async (eventId: number, quantity: number, idTicketType = 1): Promise<ApiBooking> => {
        loading.value = true
        error.value = null
        try {
            return await $fetch<ApiBooking>(`/api/bookings/${eventId}`, {
                method: 'POST',
                headers: { Authorization: `Bearer ${auth.token}`  ,   'Accept': 'application/json',
            },
                body: { id_ticket_type: idTicketType, quantity },
            })
        } catch (err: any) {
            error.value = err?.data?.detail ?? 'Erreur lors de la réservation'
            throw err
        } finally {
            loading.value = false
        }
    }

    /** DELETE /api/bookings/{event_id}?id_ticket_type=N&quantity=N — annuler une réservation */
    const cancelBooking = async (eventId: string | number, idTicketType: number, quantity: number): Promise<void> => {
        loading.value = true
        error.value = null
        try {
            await $fetch(`/api/bookings/${eventId}`, {
                method: 'DELETE',
                headers: { Authorization: `Bearer ${auth.token}`,    'Accept': 'application/json',
 },
                query: { id_ticket_type: idTicketType, quantity },
            })
        } catch (err: any) {
            error.value = err?.data?.detail ?? "Erreur lors de l'annulation"
            throw err
        } finally {
            loading.value = false
        }
    }

    return { loading, error, fetchBookings, createBooking, cancelBooking }
}