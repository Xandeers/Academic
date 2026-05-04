export type UserRole = 'client' | 'organizer'

export interface User {
  id: string
  email: string
  username: string
  description: string
  role: UserRole
  // customer only
  firstname?: string
  lastname?: string
  // organizer only
  siret?: string
}