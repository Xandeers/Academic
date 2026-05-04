export type EventCategory =
  | 'Musique' | 'Sport' | 'Culture'
  | 'E-Sport' | 'Ateliers' | 'Cinéma'

export type EventStatus = 'published' | 'draft' | 'full' | 'cancelled' | 'finished'

export interface EventTag {
  id: string // number
  label: string
}

export interface EventOrganizer {
  id: string // number
  name: string
  avatar?: string
  certified: boolean
  followersCount: number
}

export interface EventTicketType {
  id: string // number
  label: string
  price: number
  description?: string
  available: number
}

export interface Event {
  id: string // number
  title: string
  description: string
  category: EventCategory
  status: EventStatus
  date: string // date en format ISO timestamp, heure comprise, à renommer pour dire que c'est une date de début
  time: string // à remplacer par date de fin, puis à renommer du coup pour plus de sémantique
  location: string
  image?: string
  price: number
  capacity: number
  reserved: number
  organizer: EventOrganizer
  tags: EventTag[]
  ticketTypes?: EventTicketType[] // Des strings ou des IDs ?
  likesCount: number
  isFeatured?: boolean
  createdAt: string // pareil en ISO timestamp
}

/** Forme brute renvoyée par l'API FastAPI — correspond à ResponseEventSchema. */
export interface ApiEvent {
  id_event: number
  title: string
  description: string | null
  status: string
  begin_date: string
  end_date: string
  price: number
  capacity: number | null
  reserved: number
  like_count: number
  is_featured: boolean
  createdAt?: string
  /** Array d'objets {clé: valeur} p.ex. [{name:"Musique"}]. */
  category: { [key: string]: string }[]
  /** IDs numériques des lieux — PAS d'objets avec .name. */
  location_id: number[] | null
  organizer: { id_organizer: number; username: string; email?: string; siret?: string; description?: string | null }
  /** Tableau de strings simples (pas d'objets). */
  tag: string[] | null
  image: { [key: string]: string }[]
  /** Ticket types — peut être présent si l'API les retourne (non documenté dans le spec) */
  ticket_types?: { id_ticket_type: number; label: string; price: number; quantity?: number }[]
}