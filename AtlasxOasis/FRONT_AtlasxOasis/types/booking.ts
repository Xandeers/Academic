export type BookingStatus = 'confirmed' | 'cancelled' | 'pending' | 'waitlist'

/** Format brut retourné par GET /api/bookings/my-bookings (BookingResumeSchema) */
export interface ApiBooking {
  id_event: number
  id_ticket_type: number
  quantity: number
  status_ticket: string | null
}

export interface Ticket {
  id: string
  bookingId: string
  eventId: string
  idTicketType?: number  // id_ticket_type pour l'annulation
  eventTitle: string
  eventDate: string
  eventTime: string
  eventLocation: string
  eventCategory: string
  holderName: string
  ticketNumber: string
  ticketType: string
  qrCodeData: string
  price: number
}

export interface Booking {
  id: string // number
  eventId: string // number
  userId: string // number
  status: BookingStatus
  quantity: number
  totalPrice: number
  ticketTypeId?: string // number
  tickets: Ticket[]
  createdAt: string // Timestamp ISO
}

export interface WaitlistEntry {
  id: string // number
  eventId: string // number
  userId: string // number
  position: number
  createdAt: string // timestamp ISO
}