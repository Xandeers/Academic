<template>
  <div class="bg-s1 border border-white/5 rounded-2xl p-8 flex flex-col gap-6">
      <button
      @click="navigateTo('/')"
      class="flex items-center gap-1.5 text-xs text-muted hover:text-primary transition-colors w-fit"
    >
      <ArrowLeft :size="14" /> Retour
    </button>
    
    <div class="text-center">
      <h1 class="font-title text-2xl text-[#E9EEEC]">Connexion</h1>
      <p class="text-xs text-muted mt-1">Bon retour sur AtlasXOasis</p>
    </div>
    
    <div class="flex gap-2 bg-s2 rounded-lg p-1">
      <button
        :class="['flex-1 py-2 rounded-md text-xs font-title transition-all', tab === 'login' ? 'bg-s3 text-[#E9EEEC]' : 'text-muted']"
        @click="tab = 'login'"
      >Connexion</button>
      <button
        :class="['flex-1 py-2 rounded-md text-xs font-title transition-all', tab === 'register' ? 'bg-s3 text-[#E9EEEC]' : 'text-muted']"
        @click="navigateTo('/auth/register')"
      >Inscription</button>
    </div>

    <div class="flex flex-col gap-4">
      <AppInput v-model="form.email" label="Email" placeholder="vous@email.com" type="email" :error="errors.email" />
      <AppInput v-model="form.password" label="Mot de passe" placeholder="••••••••" type="password" :error="errors.password" />
    </div>

    <div v-if="authError" class="text-xs text-red-400 text-center bg-red-500/10 border border-red-500/20 rounded-lg py-2">
      {{ authError }}
    </div>

    <AppButton variant="primary" class="w-full justify-center" :loading="loading" @click="handleLogin">
      Se connecter
    </AppButton>

    <div class="flex items-center gap-3">
      <div class="flex-1 h-px bg-white/5" />
      <span class="text-xs text-muted">ou</span>
      <div class="flex-1 h-px bg-white/5" />
    </div>

    <div class="flex flex-col gap-3">
      <button class="flex items-center justify-center gap-3 bg-s2 border border-white/5 rounded-lg py-3 text-xs text-[#E9EEEC] hover:bg-s3 transition-colors">
        <img src="https://www.google.com/favicon.ico" class="w-4 h-4" />
        Continuer avec Google
      </button>
      <button class="flex items-center justify-center gap-3 bg-s2 border border-white/5 rounded-lg py-3 text-xs text-[#E9EEEC] hover:bg-s3 transition-colors">
        <span class="text-blue-400 font-title">f</span>
        Continuer avec Facebook
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import { ArrowLeft } from 'lucide-vue-next'
definePageMeta({ layout: 'auth' })

const auth = useAuthStore()
const tab = ref('login')
const loading = ref(false)
const authError = ref('')

const form = reactive({ email: '', password: '' })
const errors = reactive({ email: '', password: '' })

async function handleLogin() {
  errors.email = ''
  errors.password = ''
  authError.value = ''
  if (!form.email) { errors.email = 'Email requis'; return }
  if (!form.password) { errors.password = 'Mot de passe requis'; return }
  loading.value = true
  try {
    await auth.login(form.email, form.password)
    navigateTo('/dashboard/profile')
  } catch (e: any) {
    authError.value = e.message || 'Identifiants incorrects'
  } finally {
    loading.value = false
  }
}
</script>