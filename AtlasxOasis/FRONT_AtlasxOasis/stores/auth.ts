import { defineStore } from 'pinia'
import type { User, UserRole } from '~/types/user'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    token: null as string | null,
    isLoading: false,
    error: null as string | null,
  }),
  getters: {
    isAuthenticated: (s) => !!s.user,
    isOrganizer: (s) => s.user?.role === 'organizer',
    isClient: (s) => s.user?.role === 'client',
    fullName: (s) => s.user ? `${s.user.firstname ?? ''} ${s.user.lastname ?? ''}`.trim() || s.user.username : '',
  },
  actions: {
   async login(email: string, password: string) {
  this.isLoading = true; this.error = null
  try {
    const res: any = await $fetch('/api/auth/login', {
  method: 'POST',
  body: new URLSearchParams({ username: email, password }),
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    this.token = res.access_token

    const parts = res.access_token.split('.')
    if (parts.length !== 3 || !parts[1]) throw new Error('invalid token')
    const jwtPayload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')))
    
    const userSub = JSON.parse(jwtPayload.sub)

    this.user = {
      id: String(userSub.id_user),
      email: userSub.email,
      username: userSub.username,
      description: userSub.description ?? '',
      role: userSub.type_user === 'organizer' ? 'organizer' : 'client',
    }
    if (import.meta.client) localStorage.setItem('token', res.access_token)
  } catch (e: any) {
    this.error = e?.data?.detail ?? 'Identifiants incorrects'
    throw new Error(this.error ?? 'Erreur')
  } finally { this.isLoading = false }
},

    async register(payload: {
      firstname: string; lastname: string; username: string
      email: string; password: string; role: UserRole
      organizerSerial?: string
    }) {
      this.isLoading = true; this.error = null
      try {
        if (payload.role === 'organizer') {
          await $fetch('/api/organizers/', {
            method: 'POST',
            body: {
              username: payload.username,
              email: payload.email,
              siret: payload.organizerSerial,
              description: '',
              auth_type: 'password',
              token: payload.password,
            }
          })
        } else {
          await $fetch('/api/customers/', {
            method: 'POST',
            body: {
              firstname: payload.firstname,
              lastname: payload.lastname,
              username: payload.username,
              email: payload.email,
              description: '',
              auth_type: 'password',
              token: payload.password,
            }
          })
        }
        await this.login(payload.email, payload.password)
      } catch (e: any) {
        this.error = e?.data?.detail ?? "Erreur lors de l'inscription"
        throw new Error(this.error ?? 'Erreur')
      } finally { this.isLoading = false }
    },

    logout() {
      this.user = null
      this.token = null
      if (import.meta.client) localStorage.removeItem('token')

      navigateTo('/auth/login')
    },
    restoreSession() {
      if (!import.meta.client) return
      const saved = localStorage.getItem('token')
      if (!saved) return
      const parts = saved.split('.')
      if (parts.length !== 3 || !parts[1]) return
      try {
        const jwtPayload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')))
        const userSub = JSON.parse(jwtPayload.sub)
        this.token = saved
        this.user = {
          id: String(userSub.id_user),
          email: userSub.email,
          username: userSub.username,
          description: userSub.description ?? '',
          role: userSub.type_user === 'organizer' ? 'organizer' : 'client',
        }
      } catch { this.logout() }
    },

    clearError() { this.error = null },
  },
})