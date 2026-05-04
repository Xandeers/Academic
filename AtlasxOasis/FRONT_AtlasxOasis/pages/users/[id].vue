<template>
  <!-- Page container -->
  <div>
    <!-- Profile block -->
    <div class="bg-s1 border border-white/5 rounded-2xl flex flex-row">
      <!-- Profile picture block -->
      <div class="p-5">
        <div class="w-16 h-16 rounded-full bg-secondary/30 border border-secondary/40 flex items-center justify-center font-title text-2xl text-accent flex-shrink-0 mx-2">
          <!-- {{ initials }} -->
        </div>
      </div>

      <!-- Name and description block -->
      <div class="flex flex-col p-5 w-full">
        <h1 class="font-title mb-1">{{ user.name }}</h1>
        <p>{{ user.description }}</p>
        <AppButton class="w-[10%] my-5 max-md:w-auto" variant="ghost" @click="toggleFollow()">
          {{ user.isFollowed ? "Suivi" : "+ Suivre" }}
        </AppButton>
      </div>
    </div>

    <!-- Événéments réservés -->
    <h2 class="font-title text-2xl uppercase py-5">
      Événements réservés
    </h2>
    
    <!-- <EventGrid :events="eventTests"></EventGrid> -->
  </div>
</template>

<script setup lang="ts">
import { eventTests } from '~/mocks/events'

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();

const initials = computed((): string => {
  if (!auth.user) return '?'
  return `${auth.user.firstName[0]}${auth.user.lastName[0]}`.toUpperCase()
});

const user = reactive({
  id: 1,
  name: "Toto",
  description: "J'adore écouter de l'électronique médiévale.",
  isFollowed: false,
});

function toggleFollow(): void {
  user.isFollowed = !user.isFollowed;
}
</script>