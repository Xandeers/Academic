<template>
  <header class="sticky top-0 z-50 px-7">
    <nav class="bg-gradient-to-br from-[#1a3d2c] to-[#162e22] border border-secondary/35 rounded-xl h-[58px] flex items-center px-6 gap-5 justify-between mt-3 max-md:overflow-x-auto">

      <NuxtLink to="/" class="font-title text-accent text-base tracking-wider" style="text-shadow: 0 0 16px rgba(56,227,143,0.4)">
        AtlasXOasis
      </NuxtLink>

      <div class="flex gap-5">
        <NuxtLink to="/events" class="text-xs text-[#E9EEEC]/50 font-medium hover:text-primary transition-colors">Explorer</NuxtLink>
        <NuxtLink to="/organizers" class="text-xs text-[#E9EEEC]/50 font-medium hover:text-primary transition-colors">Organisateurs</NuxtLink>
        <!-- <NuxtLink to="/" class="text-xs text-[#E9EEEC]/50 font-medium hover:text-primary transition-colors">Calendrier</NuxtLink> -->
      </div>

      <div class="flex items-center gap-2.5">
        <div class="flex items-center gap-1.5 bg-primary/5 border border-white/10 rounded-full px-3.5 py-1.5 text-[11px] text-muted w-40 cursor-pointer">
          <Search :size="13" />
          <span>Rechercher…</span>
        </div>

        <div class="relative" ref="dropdownRef">
          <button
            v-if="auth.isAuthenticated"
            @click="showDropdown = !showDropdown"
            class="w-[34px] h-[34px] bg-secondary rounded-full flex items-center justify-center font-title text-xs text-accent"
          >
            {{ initials }}
          </button>

          <div
            v-if="showDropdown"
            class="absolute right-0 top-10 bg-s1 border border-white/10 rounded-xl p-1 flex flex-col gap-1 w-44 z-50 max-md:z-100 max-md:fixed"
          >
            <NuxtLink
              to="/dashboard/profile"
              @click="showDropdown = false"
              class="text-xs text-[#E9EEEC] hover:bg-s2 rounded-lg px-3 py-2 transition-colors"
            >
               Mon profil
            </NuxtLink>
            <NuxtLink
              to="/dashboard"
              @click="showDropdown = false"
              class="text-xs text-[#E9EEEC] hover:bg-s2 rounded-lg px-3 py-2 transition-colors"
            >
               Dashboard
            </NuxtLink>
            <div class="h-px bg-white/5 my-1" />
            <button
              @click="auth.logout(); showDropdown = false"
              class="text-xs text-red-400 hover:bg-red-500/10 rounded-lg px-3 py-2 transition-colors text-left"
            >
               Se déconnecter
            </button>
          </div>

          <NuxtLink v-if="!auth.isAuthenticated" to="/auth/login"
            class="bg-accent text-[#0b2618] rounded-full px-4 py-1.5 font-title text-[11px] no-underline">
            Mon compte
          </NuxtLink>
        </div>

      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { Search } from 'lucide-vue-next'

const auth = useAuthStore()
const showDropdown = ref(false)
const dropdownRef = ref(null)

const initials = computed(() => {
  if (!auth.user) return ''
  return auth.user.username.slice(0, 2).toUpperCase()
})

onMounted(() => {
  document.addEventListener('click', (e) => {
    if (dropdownRef.value && !(dropdownRef.value as any).contains(e.target)) {
      showDropdown.value = false
    }
  })
})
</script>