<template>
  <div class="min-h-screen bg-bg px-5 py-10">
    <div class="max-w-4xl mx-auto">

      <!-- Header -->
      <div class="mb-12">
        <h1 class="font-title text-4xl text-[#E9EEEC] uppercase tracking-wide mb-2">
          Créer un événement
        </h1>
        <p class="text-muted">Publiez votre événement en 4 étapes simples</p>
      </div>

      <!-- Progress Indicator -->
      <div class="mb-12">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-title text-muted uppercase tracking-widest">Étape {{ currentStep }} / 4</span>
          <span class="text-sm font-title text-accent uppercase tracking-widest">{{ stepTitles[currentStep - 1] }}</span>
        </div>
        <div class="h-1.5 bg-secondary/15 rounded-full overflow-hidden">
          <div
            class="h-full bg-accent transition-all duration-500"
            :style="{ width: (currentStep / 4) * 100 + '%' }"
          />
        </div>
      </div>

      <!-- Form Container -->
      <div class="bg-s1 border border-white/5 rounded-2xl p-8">

        <!-- STEP 1: Infos générales -->
        <div v-if="currentStep === 1" class="space-y-6">
          <h2 class="font-title text-2xl text-[#E9EEEC] uppercase tracking-wide mb-8">Informations générales</h2>
          
          <AppInput
            v-model="form.title"
            label="Titre de l'événement"
            placeholder="Ex: Concert Été 2026"
            @blur="validateTitle"
          />
          <div v-if="errors.title" class="text-red-400 text-sm">{{ errors.title }}</div>

          <div>
            <label class="block text-sm font-title text-muted uppercase tracking-widest mb-3">
              Catégorie
            </label>
            <AppSelect
              v-model="form.category"
              :options="categoryOptions"
            />
          </div>

          <AppInput
            v-model="form.description"
            label="Description"
            placeholder="Décrivez votre événement..."
            type="textarea"
            rows="5"
            @blur="validateDescription"
          />
          <div v-if="errors.description" class="text-red-400 text-sm">{{ errors.description }}</div>
        </div>

        <!-- STEP 2: Date, heure, lieu -->
        <div v-if="currentStep === 2" class="space-y-6">
          <h2 class="font-title text-2xl text-[#E9EEEC] uppercase tracking-wide mb-8">Date & Lieu</h2>

          <div class="grid grid-cols-2 gap-4">
            <AppInput
              v-model="form.date"
              label="Date de début"
              type="date"
              @blur="validateDate"
            />
            <AppInput
              v-model="form.time"
              label="Heure de début"
              type="time"
              @blur="validateTime"
            />
            <AppInput
              v-model="form.endDate"
              label="Date de fin"
              type="date"
            />
            <AppInput
              v-model="form.endTime"
              label="Heure de fin"
              type="time"
            />
          </div>
          <div v-if="errors.date" class="text-red-400 text-sm">{{ errors.date }}</div>
          <div v-if="errors.time" class="text-red-400 text-sm">{{ errors.time }}</div>

          <AppInput
            v-model="form.location"
            label="Lieu"
            placeholder="Ex: Paris - La Défense"
            @blur="validateLocation"
          />
          <div v-if="errors.location" class="text-red-400 text-sm">{{ errors.location }}</div>
        </div>

        <!-- STEP 3: Billets & Capacité -->
        <div v-if="currentStep === 3" class="space-y-6">
          <h2 class="font-title text-2xl text-[#E9EEEC] uppercase tracking-wide mb-8">Billets & Capacité</h2>

          <AppInput
            v-model="form.capacity"
            label="Capacité totale"
            type="number"
            placeholder="500"
            @blur="validateCapacity"
          />
          <div v-if="errors.capacity" class="text-red-400 text-sm">{{ errors.capacity }}</div>

          <AppInput
            :modelValue="String(form.price || '')"
            @update:modelValue="form.price = Number($event) || 0"
            label="Prix de base (€)"
            type="number"
            placeholder="0 = Gratuit"
          />

          <!-- Ticket Types -->
          <div>
            <div class="flex items-center justify-between mb-4">
              <h3 class="font-title text-lg text-[#E9EEEC] uppercase tracking-wide">Types de billets</h3>
              <AppButton
                variant="dark"
                @click="addTicketType"
                :disabled="form.ticketTypes.length >= 5"
              >
                + Ajouter un type
              </AppButton>
            </div>

            <div class="space-y-4">
              <div
                v-for="(ticket, idx) in form.ticketTypes"
                :key="idx"
                class="bg-bg/50 border border-secondary/20 rounded-xl p-4 space-y-3"
              >
                <div class="flex items-start justify-between">
                  <div class="flex-1 space-y-3">
                    <AppInput
                      v-model="ticket.label"
                      label="Nom du ticket"
                      placeholder="Ex: VIP"
                      size="sm"
                    />
                    <div class="grid grid-cols-2 gap-3">
                      <AppInput
                        :modelValue="String(ticket.price || '')"
                        @update:modelValue="ticket.price = $event as any"
                        label="Prix (€)"
                        type="number"
                        placeholder="50"
                        size="sm"
                      />
                      <AppInput
                        :modelValue="String(ticket.available || '')"
                        @update:modelValue="ticket.available = $event as any"
                        label="Nombre"
                        type="number"
                        placeholder="100"
                        size="sm"
                      />
                    </div>
                    <AppInput
                      v-model="ticket.description"
                      label="Description"
                      placeholder="Ex: Front row + cocktail gratuit"
                      size="sm"
                    />
                  </div>
                  <button
                    @click="removeTicketType(idx)"
                    class="text-red-400 hover:text-red-300 p-2 rounded transition-colors"
                  >
                    ✕
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- STEP 4: Récapitulatif & Publication -->
        <div v-if="currentStep === 4" class="space-y-6">
          <h2 class="font-title text-2xl text-[#E9EEEC] uppercase tracking-wide mb-8">Récapitulatif</h2>

          <!-- Event Summary -->
          <div class="space-y-4">
            <div class="bg-bg/50 border border-secondary/20 rounded-xl p-6">
              <h3 class="font-title text-xl text-accent mb-4">{{ form.title }}</h3>
              <p class="text-muted text-sm mb-6 line-clamp-3">{{ form.description }}</p>
              
              <div class="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <span class="text-xs text-muted font-title uppercase tracking-widest">Catégorie</span>
                  <p class="text-[#E9EEEC] font-semibold">{{ form.category }}</p>
                </div>
                <div>
                  <span class="text-xs text-muted font-title uppercase tracking-widest">Date & Heure</span>
                  <p class="text-[#E9EEEC] font-semibold">{{ new Date(form.date).toLocaleDateString('fr-FR') }} à {{ form.time }}</p>
                </div>
                <div class="col-span-2">
                  <span class="text-xs text-muted font-title uppercase tracking-widest">Lieu</span>
                  <p class="text-[#E9EEEC] font-semibold">{{ form.location }}</p>
                </div>
              </div>

              <div class="border-t border-secondary/20 pt-4">
                <span class="text-xs text-muted font-title uppercase tracking-widest">Capacité</span>
                <p class="text-[#E9EEEC] font-semibold">{{ parseInt(form.capacity) || 0 }} places</p>
              </div>
            </div>

            <!-- Ticket Types Summary -->
            <div v-if="form.ticketTypes.length > 0">
              <h4 class="font-title text-lg text-[#E9EEEC] uppercase tracking-wide mb-3">Types de billets</h4>
              <div class="space-y-2">
                <div
                  v-for="(ticket, idx) in form.ticketTypes"
                  :key="idx"
                  class="bg-bg/50 border border-secondary/20 rounded-lg p-3 flex justify-between items-center"
                >
                  <div>
                    <p class="font-semibold text-[#E9EEEC]">{{ ticket.label }}</p>
                    <p class="text-sm text-muted">{{ parseInt(ticket.available as any) || 0 }} places - {{ parseInt(ticket.price as any) || 0 }}€</p>
                  </div>
                  <span class="text-accent font-title">{{ parseInt(ticket.price as any) || 0 }}€</span>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-accent/10 border border-accent/20 rounded-xl p-4">
            <p class="text-sm text-[#E9EEEC]">
              En cliquant sur "Publier", votre événement sera visible pour tous les utilisateurs.
            </p>
          </div>
        </div>

        <!-- Navigation Buttons -->
        <div class="flex gap-3 justify-between mt-12 pt-8 border-t border-secondary/15">
          <AppButton
            v-if="currentStep > 1"
            variant="ghost"
            @click="previousStep"
          >
            ← Précédent
          </AppButton>
          <div v-else />

          <div class="flex gap-3">
            <AppButton
              v-if="currentStep < 4"
              variant="primary"
              @click="nextStep"
              :disabled="!isStepValid"
            >
              Suivant →
            </AppButton>
            <AppButton
              v-else
              variant="primary"
              @click="publishEvent"
              :loading="isPublishing"
            >
              Publier l'événement
            </AppButton>
          </div>
        </div>

        <!-- Erreur publication -->
        <div v-if="publishError" class="mt-4 p-3 rounded-lg bg-red-500/10 border border-red-500/25 text-red-400 text-sm">
          {{ publishError }}
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { EventCategory, EventTicketType } from '~/types/event'
import AppButton from '~/components/ui/AppButton.vue'
import AppInput from '~/components/ui/AppInput.vue'
import AppSelect from '~/components/ui/AppSelect.vue'

definePageMeta({ layout: 'default', middleware: 'auth' })

const router = useRouter()
const auth = useAuthStore()

const currentStep = ref(1)
const isPublishing = ref(false)
const publishError = ref<string | null>(null)

const stepTitles = [
  'Infos générales',
  'Date & Lieu',
  'Billets & Capacité',
  'Récapitulatif'
]

// Catégories depuis l'API
const categoriesFromApi = ref<{ id_category: number; label: string }[]>([])
const categoryOptions = computed(() =>
  categoriesFromApi.value.length
    ? categoriesFromApi.value.map(c => ({ label: c.label, value: c.label }))
    : [
        { label: 'Musique', value: 'Musique' },
        { label: 'Sport', value: 'Sport' },
        { label: 'Culture', value: 'Culture' },
        { label: 'E-Sport', value: 'E-Sport' },
        { label: 'Ateliers', value: 'Ateliers' },
        { label: 'Cinéma', value: 'Cinéma' },
      ]
)

onMounted(async () => {
  try {
    categoriesFromApi.value = await $fetch<{ id_category: number; label: string }[]>('/api/category/')
  } catch { /* fallback to hardcoded */ }
})

const form = ref({
  title: '',
  description: '',
  category: 'Musique' as EventCategory,
  date: '',
  time: '',
  endDate: '',
  endTime: '',
  location: '',
  capacity: '',
  price: 0,
  ticketTypes: [] as EventTicketType[]
})

const errors = ref({
  title: '',
  description: '',
  date: '',
  time: '',
  location: '',
  capacity: ''
})

// Validations
const validateTitle = () => {
  if (!form.value.title.trim()) {
    errors.value.title = 'Le titre est requis'
  } else if (form.value.title.length < 3) {
    errors.value.title = 'Le titre doit contenir au moins 3 caractères'
  } else {
    errors.value.title = ''
  }
}

const validateDescription = () => {
  if (!form.value.description.trim()) {
    errors.value.description = 'La description est requise'
  } else if (form.value.description.length < 10) {
    errors.value.description = 'La description doit contenir au moins 10 caractères'
  } else {
    errors.value.description = ''
  }
}

const validateDate = () => {
  if (!form.value.date) {
    errors.value.date = 'La date est requise'
  } else if (new Date(form.value.date) <= new Date()) {
    errors.value.date = 'La date doit être dans le futur'
  } else {
    errors.value.date = ''
  }
}

const validateTime = () => {
  if (!form.value.time) {
    errors.value.time = 'L\'heure est requise'
  } else {
    errors.value.time = ''
  }
}

const validateLocation = () => {
  if (!form.value.location.trim()) {
    errors.value.location = 'Le lieu est requis'
  } else {
    errors.value.location = ''
  }
}

const validateCapacity = () => {
  const capacity = parseInt(form.value.capacity) || 0
  if (!form.value.capacity || capacity <= 0) {
    errors.value.capacity = 'La capacité doit être supérieure à 0'
  } else {
    errors.value.capacity = ''
  }
}

// Step validation
const isStepValid = computed(() => {
  switch (currentStep.value) {
    case 1:
      return form.value.title.trim() && form.value.description.trim() && !errors.value.title && !errors.value.description
    case 2:
      return form.value.date && form.value.time && form.value.location && !errors.value.date && !errors.value.time && !errors.value.location
    case 3:
      return parseInt(form.value.capacity) > 0 && !errors.value.capacity
    case 4:
      return true
    default:
      return false
  }
})

const nextStep = () => {
  if (currentStep.value < 4) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const addTicketType = () => {
  if (form.value.ticketTypes.length < 5) {
    form.value.ticketTypes.push({
      id: `ticket_${Date.now()}`,
      label: '',
      price: 0,
      description: '',
      available: 0
    })
  }
}

const removeTicketType = (idx: number) => {
  form.value.ticketTypes.splice(idx, 1)
}

const publishEvent = async () => {
  isPublishing.value = true
  publishError.value = null
  try {
    // Construire les timestamps ISO
    const beginDate = form.value.date && form.value.time
      ? `${form.value.date}T${form.value.time}:00`
      : form.value.date ? `${form.value.date}T00:00:00` : ''
    const endRaw = form.value.endDate || form.value.date
    const endTimeRaw = form.value.endTime || form.value.time || '23:59'
    const endDate = endRaw ? `${endRaw}T${endTimeRaw}:00` : ''

    // Trouver l'id_category correspondant au label choisi
    const catMatch = categoriesFromApi.value.find(c => c.label === form.value.category)
    const idCategory = catMatch?.id_category

    const payload: Record<string, any> = {
      name: form.value.title,
      description: form.value.description,
      start_date: beginDate,
      end_date: endDate,
      created_date: new Date().toISOString(),
      event_status: 'published',
      max_capacity: parseInt(form.value.capacity) || 0,
      metadata: {},
    }
    if (idCategory) payload.id_category = idCategory

    const locationBody: Record<string, any> = {
      max_capacity: payload.max_capacity,
      name: form.value.location,
      address: form.value.location,
      city: "Lyon",
      postal_code: "69000",
      longitude: 0,
      latitude: 0,
      accessibility: true,
      nearby_transport: "bus"
    }

    await $fetch('/api/events/', {
      method: 'POST',
      headers: { Authorization: `Bearer ${auth.token}` },
      body: payload,
    })

    await $fetch('/api/locations/', {
      method: 'POST',
      body: locationBody
    })

    const events = await $fetch('/api/events/')
    const latestEvent = events.sort((a, b) => Number(a.id_event) - Number(b.id_event))[events.length - 1]

    const locations = await $fetch('/api/locations/')
    const latestLocation = locations.sort((a, b) => Number(a.id_location) - Number(b.id_location))[locations.length - 1]

    await $fetch(`/api/events/${latestEvent.id_event}/category/${idCategory}`, {
      method: 'POST',
    })

    await $fetch(`/api/events/${latestEvent.id_event}/location/${latestLocation.id_location}`, {
      method: 'POST',
    })

    await router.push('/dashboard/events')
  } catch (err: any) {
    publishError.value = err?.data?.detail ?? 'Erreur lors de la création de l\'\u00e9vénement'
  } finally {
    isPublishing.value = false
  }
}
</script> 
