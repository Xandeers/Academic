<template>
  <!-- Page container -->
  <div>
    <!-- Profile block -->
    <div class="flex flex-col bg-s1 border border-white/5 rounded-xl p-5 my-5">
      <!-- Image / Name / Desc block -->
      <div class="flex flex-row">
        <!-- Profile picture block -->
        <!-- <div class="flex flex-col">
          <NuxtImg 
            :src="organizer.image"
            alt="logo DJ Collective Lyon"
            width="200"
            class="p-5"
          />
        </div> -->

        <!-- Name and description block -->
        <div class="flex flex-col p-5">
          <h1 class="font-title mb-1">{{ organizer.username }}</h1>
          <p>{{ organizer.description }}</p>
        </div>
      </div>

      <!-- Followers / Follow block -->
      <div class="flex flex-row items-center">
        <p>♥ {{ formatFrenchNumber(organizer.nb_follower) }}</p>
        <button
          :class="[
            'ml-auto px-4 py-1.5 rounded-lg border text-xs transition-all',
            isFollowedRef
              ? 'bg-secondary/25 border-secondary/40 text-primary'
              : 'bg-secondary/15 border-secondary/25 text-accent hover:bg-secondary/25'
          ]"
          @click="toggleFollow"
        >
          {{ isFollowedRef ? '✓ Suivi' : '+ Suivre' }}
        </button>
      </div>
    </div> 

    <h2 class="font-title mb-2">Événements organisés</h2>
    <EventGrid :events="events"></EventGrid>
  </div>
</template>

<script setup lang="ts">
import { Search, Heart } from 'lucide-vue-next'

import { eventTests } from '~/mocks/events';

definePageMeta({layout: 'default'})

const eventsStore = useEventsStore();
await callOnce(eventsStore.fetchEvents)

const route = useRoute();
const router = useRouter();

const { data: organizer, error } = await useFetch(`/api/organizers/${route.params.id}`, {
  key: `organizer-page-${route.params.id}`,
}) 

const events = eventsStore.events.filter((event) => Number(event.organizer.id_organizer) === Number(route.params.id))

const auth = useAuthStore()

const { data: followers, refresh: refreshFollowers } = await useFetch(`/api/users/${route.params.id}/followers`)

const isFollowedRef = computed(() => {
  if (!auth.user?.id || !followers.value) return false 

  return followers.value.some(
    f => Number(f.follower_customer.id_customer) === Number(auth.user.id)
  )
})

async function toggleFollow() {
  if (!auth.isAuthenticated) return navigateTo('/auth/login')

  if (!isFollowedRef.value) {
    await $fetch(`/api/users/${route.params.id}/follow`, { 
      method: 'POST',  
      headers: { Authorization: `Bearer ${auth.token}` },
      body: { status_follow: "followed" }
    })
  } else {
    await $fetch(`/api/users/${route.params.id}/unfollow`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${auth.token} `}
    })
  }
  await refreshFollowers()
}

/*
En attendant l'API
Un organisateur doit au moins avoir :
- Id
- Nom
- Avatar
- Description
- Events publiés
- Nombre followers
- Certifié ou non
- Est suivi ou non par l'utilisateur courant

Sur l'interface
- Bouton suivre
*/
// const organizer = reactive({
//   id: 1,
//   name: 'DJ Collective Lyon',
//   image: "/img/organizers/organizer1.png",
//   description: "Groupe indépendant de DJ lyonnais spécialisé dans la phonk tibétaine",
//   events: eventTests,
//   // Le _ n'est pas lu par TS, c'est juste pour la lisibilité humaine
//   followersCount: 200_000,
//   certified: true,
//   isFollowed: false,
// });

</script>