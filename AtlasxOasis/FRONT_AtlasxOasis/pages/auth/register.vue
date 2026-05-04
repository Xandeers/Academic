<template>
  <button
      @click="navigateTo('/')"
      class="flex items-center gap-1.5 text-xs text-muted hover:text-primary transition-colors w-fit"
    >
      <ArrowLeft :size="14" /> Retour
    </button>
  <div class="bg-s1 border border-white/5 rounded-2xl p-8 flex flex-col gap-6">
    <div class="text-center">
      <h1 class="font-title text-2xl text-[#E9EEEC]">Créer un compte</h1>
      <p class="text-xs text-muted mt-1">Rejoignez AtlasXOasis</p>
    </div>

    <div class="flex gap-2 bg-s2 rounded-lg p-1">
      <button class="flex-1 py-2 rounded-md text-xs font-title text-muted" @click="navigateTo('/auth/login')">
        Connexion
      </button>
      <button class="flex-1 py-2 rounded-md text-xs font-title bg-s3 text-[#E9EEEC]">
        Inscription
      </button>
    </div>

    <div class="flex gap-3">
      <AppInput v-model="form.firstname" label="Prénom" placeholder="Jean" class="flex-1" :error="errors.firstname" />
      <AppInput v-model="form.lastname" label="Nom" placeholder="Dupont" class="flex-1" :error="errors.lastname" />
    </div>
    <AppInput v-model="form.username" label="Pseudo " placeholder="@monpseudo" />
    <AppInput v-model="form.email" label="Email" placeholder="vous@email.com" type="email" :error="errors.email" />
    <AppInput v-model="form.password" label="Mot de passe" placeholder="••••••••" type="password" :error="errors.password" />
    <AppInput v-model="form.confirm" label="Confirmer le mot de passe" placeholder="••••••••" type="password" :error="errors.confirm" />
     <AppInput v-if="form.role === 'organizer'" v-model="form.organizerSerial"  label="Numéro SIRET / Série"  placeholder="123 456 789 00012" :error="errors.organizerSerial" />
    <div class="flex flex-col gap-2">
      <label class="text-xs font-semibold text-[#E9EEEC]/60 tracking-wide">Je suis</label>
      <div class="flex gap-3">
        <button
          :class="['flex-1 py-3 rounded-lg border text-xs font-title transition-all', form.role === 'client' ? 'bg-accent/10 border-accent/30 text-accent' : 'bg-s2 border-white/5 text-muted']"
          @click="form.role = 'client'"
        >
          👤 Participant
        </button>
        <button
          :class="['flex-1 py-3 rounded-lg border text-xs font-title transition-all', form.role === 'organizer' ? 'bg-accent/10 border-accent/30 text-accent' : 'bg-s2 border-white/5 text-muted']"
          @click="form.role = 'organizer'"
        >
          🎤 Organisateur
        </button>
      </div>
    </div>

    <div v-if="authError" class="text-xs text-red-400 text-center bg-red-500/10 border border-red-500/20 rounded-lg py-2">
      {{ authError }}
    </div>

    <AppButton variant="primary" class="w-full justify-center" :loading="loading" @click="handleRegister">
      Créer mon compte
    </AppButton>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import { ArrowLeft } from 'lucide-vue-next'
import type { UserRole } from '~/types/user'
definePageMeta({ layout: 'auth' })

const auth = useAuthStore()
const loading = ref(false)
const authError = ref('')

const form = reactive({
  firstname: '', lastname: '', username: '',
  email: '', password: '', confirm: '',
  role: 'client' as UserRole,
  organizerSerial: ''
})
const errors = reactive({
  firstname: '', lastname: '', username: '',
  email: '', password: '', confirm: '', organizerSerial: ''
})

async function handleRegister() {
  Object.keys(errors).forEach(k => (errors as any)[k] = '')
  authError.value = ''
  if (!form.firstname) { errors.firstname = 'Requis'; return }
  if (!form.lastname) { errors.lastname = 'Requis'; return }
  if (!form.username) { errors.username = 'Requis'; return }
  if (!form.email) { errors.email = 'Requis'; return }
  if (!form.password) { errors.password = 'Requis'; return }
  if (form.password !== form.confirm) { errors.confirm = 'Les mots de passe ne correspondent pas'; return }
  if (form.role === 'organizer' && !form.organizerSerial) { errors.organizerSerial = 'Requis'; return }
  loading.value = true
  try {
    await auth.register({ ...form })
    navigateTo('/dashboard/profile')
  } catch (e: any) {
    authError.value = e.message || 'Erreur lors de la création du compte'
  } finally {
    loading.value = false
  }
}
</script>