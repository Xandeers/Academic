<template>
  <div class="border border-accent/10 rounded-xl bg-gradient-to-br from-surface-1 to-surface-2 p-6 flex flex-col gap-6">
    <!-- Header -->
    <div class="flex flex-col gap-2">
      <h3 class="font-title text-lg font-black text-white uppercase tracking-wide">Réserver vos places</h3>
      <p class="text-sm text-muted leading-relaxed">Sélectionnez le type de billet et la quantité désirée</p>
    </div>

    <!-- Form -->
    <form @submit.prevent="handleSubmit" class="flex flex-col gap-5">
      <!-- Ticket Type Selection -->
      <div class="flex flex-col gap-3">
        <div class="p-4 bg-accent/5 border border-accent/20 rounded-lg">
          <p class="text-sm text-[#E9EEEC] font-semibold">Billet standard — {{ props.event.price?.toFixed(2) ?? '0.00' }} €</p>
        </div>
      </div>

      <!-- Quantity Selection -->
      <div class="flex flex-col gap-3 w-full">
        <label class="font-title text-[9px] tracking-[0.14em] uppercase text-accent/80">
          Quantité
        </label>
        <div class="flex gap-3">
          <button
            type="button"
            @click="decreaseQuantity"
            :disabled="quantity <= 1 || isLoading"
            class="flex-1 flex items-center justify-center bg-surface-1 border border-white/10 rounded-lg px-4 py-3 text-accent hover:border-accent/50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors duration-200"
          >
            −
          </button>
          <div class="flex-1 flex items-center justify-center bg-surface-1 border border-white/10 rounded-lg px-4 py-3 text-white text-sm font-semibold">
            {{ quantity }}
          </div>
          <button
            type="button"
            @click="increaseQuantity"
            :disabled="quantity >= maxAvailable || isLoading"
            class="flex-1 flex items-center justify-center bg-surface-1 border border-white/10 rounded-lg px-4 py-3 text-accent hover:border-accent/50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors duration-200"
          >
            +
          </button>
        </div>
        <p class="text-[11px] text-muted">
          {{ maxAvailable }} {{ maxAvailable > 1 ? 'places disponibles' : 'place disponible' }}
        </p>
      </div>

      <!-- Price Summary -->
      <div class="bg-surface-0/50 border border-accent/10 rounded-lg p-4 flex flex-col gap-3">
        <div class="flex justify-between items-center gap-3">
          <span class="text-sm text-muted">Prix unitaire</span>
          <span class="font-title text-sm text-white">{{ (props.event.price ?? 0).toFixed(2) }} €</span>
        </div>
        <div class="flex justify-between items-center gap-3">
          <span class="text-sm text-muted">Quantité</span>
          <span class="font-title text-sm text-white">{{ quantity }}</span>
        </div>
        <div class="h-px bg-accent/10" />
        <div class="flex justify-between items-center gap-3 pt-2">
          <span class="font-title text-sm uppercase tracking-wider">Prix total</span>
          <span class="font-title text-lg text-accent">{{ totalPrice.toFixed(2) }} €</span>
        </div>
      </div>

      <!-- Submit Button -->
      <AppButton
        type="submit"
        variant="primary"
        :disabled="isLoading"
        :loading="isLoading"
        class="w-full mt-1"
      >
        {{ isLoading ? 'Réservation en cours...' : 'Confirmer la réservation' }}
      </AppButton>

      <!-- Error Message -->
      <div v-if="errorMessage" class="p-3 bg-red-500/10 border border-red-500/25 rounded-lg mt-2">
        <p class="text-sm text-red-400">{{ errorMessage }}</p>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import type { Event, EventTicketType } from '~/types/event'
import { useBooking } from '~/composables/useBooking'
import { useAuthStore } from '~/stores/auth'
import AppSelect from '~/components/ui/AppSelect.vue'
import AppButton from '~/components/ui/AppButton.vue'

const router = useRouter()
const authStore = useAuthStore()
const props = defineProps<{
  event: Event
}>()

const emit = defineEmits<{
  success: [booking: any]
  error: [message: string]
}>()

// Composable hook
const { createBooking, loading: bookingLoading } = useBooking()

// State
const selectedTicketTypeId = ref<string>('')
const quantity = ref<number>(1)
const isLoading = ref(false)
const errorMessage = ref<string>('')

// Computed properties
const selectedTicketType = computed(() => {
  return props.event.ticketTypes?.find(t => t.id === selectedTicketTypeId.value)
})

const maxAvailable = computed(() => {
  return props.event.capacity ? props.event.capacity - props.event.reserved : 100
})

const totalPrice = computed(() => {
  return (props.event.price ?? 0) * quantity.value
})

const ticketTypeOptions = computed(() => {
  return (props.event.ticketTypes ?? []).map(type => ({
    value: type.id,
    label: `${type.label}${type.description ? ' - ' + type.description : ''} (${type.price.toFixed(2)} €)`
  }))
})

// Methods
const increaseQuantity = () => {
  if (quantity.value < maxAvailable.value) {
    quantity.value++
    errorMessage.value = ''
  }
}

const decreaseQuantity = () => {
  if (quantity.value > 1) {
    quantity.value--
    errorMessage.value = ''
  }
}

const handleSubmit = async () => {
  if (quantity.value < 1) {
    errorMessage.value = 'La quantité doit être au moins 1'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const booking = await createBooking({
      eventId: String(props.event.id),
      ticketTypeId: String(1), // default ticket type
      quantity: quantity.value,
      totalPrice: (props.event.price ?? 0) * quantity.value,
      eventTitle: props.event.title,
      eventBeginDate: props.event.date,
      eventEndDate: props.event.time,
      eventLocation: props.event.location,
      eventCategory: props.event.category,
      holderName: authStore.fullName || authStore.user?.email || 'Participant',
    })

    emit('success', booking)

    // Redirection vers la page de confirmation avec l'event_id
    setTimeout(() => {
      router.push(`/booking/${props.event.id}`)
    }, 500)
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Une erreur s\'est produite lors de la réservation'
    errorMessage.value = message
    emit('error', message)
  } finally {
    isLoading.value = false
  }
}

// Reset form when event changes
watch(() => props.event.id, () => {
  selectedTicketTypeId.value = ''
  quantity.value = 1
  errorMessage.value = ''
})
</script>
