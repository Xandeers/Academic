<template>
  <div class="booking-ticket">
    <!-- Ticket Card -->
    <div class="booking-ticket__card">
      <!-- Header with Category Badge -->
      <div class="booking-ticket__header">
        <div class="booking-ticket__category">{{ ticket.eventCategory }}</div>
        <div class="booking-ticket__ticket-type">{{ ticket.ticketType }}</div>
      </div>

      <!-- Event Title -->
      <div class="booking-ticket__event-title">{{ ticket.eventTitle }}</div>

      <!-- Event Details -->
      <div class="booking-ticket__details-grid">
        <div class="booking-ticket__detail-item">
          <span class="booking-ticket__detail-label">Date</span>
          <span class="booking-ticket__detail-value">{{ ticket.eventDate }}</span>
        </div>
        <div class="booking-ticket__detail-item">
          <span class="booking-ticket__detail-label">Heure</span>
          <span class="booking-ticket__detail-value">{{ ticket.eventTime }}</span>
        </div>
        <div class="booking-ticket__detail-item">
          <span class="booking-ticket__detail-label">Lieu</span>
          <span class="booking-ticket__detail-value">{{ ticket.eventLocation }}</span>
        </div>
      </div>

      <!-- QR Code & Holder Info -->
      <div class="booking-ticket__content">
        <div class="booking-ticket__holder">
          <div class="booking-ticket__label">Détenteur</div>
          <div class="booking-ticket__holder-name">{{ ticket.holderName }}</div>
          <div class="booking-ticket__ticket-number">
            <span class="text-xs text-muted uppercase">N° Billet:</span>
            <span class="font-mono text-accent">{{ ticket.ticketNumber }}</span>
          </div>
        </div>

        <div class="booking-ticket__qr">
          <AppQRCode
            :value="ticket.qrCodeData"
            :size="200"
            alt="QR Code du billet"
          />
        </div>
      </div>

      <!-- Divider -->
      <div class="booking-ticket__divider" />

      <!-- Footer Info -->
      <div class="booking-ticket__footer">
        <div class="booking-ticket__footer-item">
          <span class="booking-ticket__label">Prix</span>
          <span class="booking-ticket__price">{{ ticket.price.toFixed(2) }} €</span>
        </div>
        <div class="booking-ticket__footer-item">
          <span class="booking-ticket__label">Status</span>
          <span class="booking-ticket__status">✓ Valid</span>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="booking-ticket__actions" v-if="showActions">
      <AppButton
        variant="primary"
        class="flex-1"
        @click="downloadPDF"
        :loading="loadingPDF"
      >
         Télécharger PDF
      </AppButton>
      <AppButton
        variant="ghost"
        class="flex-1"
        @click="downloadImage"
        :loading="loadingImage"
      >
         Télécharger Image
      </AppButton>
      <AppButton
        variant="dark"
        class="flex-1"
        @click="printTicket"
      >
         Imprimer
      </AppButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Ticket } from '~/types/booking'
import { generateTicketPDF, downloadTicketAsImage } from '~/utils/generateTicketPDF'
import AppQRCode from '~/components/ui/AppQRCode.vue'
import AppButton from '~/components/ui/AppButton.vue'

const props = defineProps<{
  ticket: Ticket
  showActions?: boolean
}>()

const loadingPDF = ref(false)
const loadingImage = ref(false)

const downloadPDF = async () => {
  loadingPDF.value = true
  try {
    await generateTicketPDF(
      props.ticket,
      `billet-${props.ticket.ticketNumber}.pdf`
    )
  } catch (error) {
    console.error('Erreur:', error)
    alert('Impossible de télécharger le PDF')
  } finally {
    loadingPDF.value = false
  }
}

const downloadImage = async () => {
  loadingImage.value = true
  try {
    await downloadTicketAsImage(props.ticket)
  } catch (error) {
    console.error('Erreur:', error)
    alert('Impossible de télécharger l\'image')
  } finally {
    loadingImage.value = false
  }
}

const printTicket = () => {
  window.print()
}
</script>

<style scoped>
.booking-ticket {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.booking-ticket__card {
  border: 2px solid rgba(56, 227, 143, 0.2);
  border-radius: 16px;
  background: linear-gradient(135deg, #242624 0%, #2C2E2C 100%);
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.booking-ticket__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.booking-ticket__category {
  font-family: 'Archivo Black', sans-serif;
  font-size: 9px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  background: rgba(56, 227, 143, 0.15);
  color: #38E38F;
  padding: 4px 10px;
  border-radius: 20px;
}

.booking-ticket__ticket-type {
  font-size: 11px;
  color: #99D7B8;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.booking-ticket__event-title {
  font-family: 'Archivo Black', sans-serif;
  font-size: 28px;
  font-weight: 900;
  color: #E9EEEC;
  line-height: 1.2;
}

.booking-ticket__details-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding: 20px;
  background: rgba(51, 53, 51, 0.5);
  border-radius: 12px;
  border: 1px solid rgba(153, 215, 184, 0.12);
}

.booking-ticket__detail-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.booking-ticket__detail-label {
  font-size: 9px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #6B7A72;
}

.booking-ticket__detail-value {
  font-size: 14px;
  font-weight: 600;
  color: #E9EEEC;
}

.booking-ticket__content {
  display: grid;
  grid-template-columns: 1fr 220px;
  gap: 32px;
  align-items: start;
  padding-bottom: 24px;
}

.booking-ticket__holder {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.booking-ticket__label {
  font-size: 9px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #6B7A72;
  font-weight: 600;
}

.booking-ticket__holder-name {
  font-size: 20px;
  font-weight: bold;
  color: #38E38F;
  line-height: 1.3;
}

.booking-ticket__ticket-number {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding-top: 8px;
  border-top: 1px solid rgba(153, 215, 184, 0.12);
}

.booking-ticket__qr {
  display: flex;
  justify-content: center;
}

.booking-ticket__divider {
  height: 2px;
  background: linear-gradient(90deg, rgba(56, 227, 143, 0.1) 0%, rgba(56, 227, 143, 0.3) 50%, rgba(56, 227, 143, 0.1) 100%);
}

.booking-ticket__footer {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.booking-ticket__footer-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.booking-ticket__price {
  font-size: 18px;
  font-weight: bold;
  color: #38E38F;
}

.booking-ticket__status {
  font-size: 14px;
  color: #38E38F;
  font-weight: 600;
}

.booking-ticket__actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

@media (max-width: 768px) {
  .booking-ticket__card {
    padding: 20px;
  }

  .booking-ticket__details-grid {
    grid-template-columns: 1fr;
  }

  .booking-ticket__content {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .booking-ticket__actions {
    grid-template-columns: 1fr;
  }
}

@media print {
  .booking-ticket__actions {
    display: none;
  }
}
</style>
