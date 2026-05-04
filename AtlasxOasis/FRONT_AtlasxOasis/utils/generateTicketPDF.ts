import type { Ticket } from '~/types/booking'

/**
 * genère un PDF du billet
 * Ouvre l'impression navigateur pour télécharger/imprimer
 * @param ticket - Le billet à convertir en PDF
 * @param fileName 
 */
export const generateTicketPDF = async (ticket: Ticket, fileName?: string): Promise<void> => {
    downloadTicketAsScreenshot(ticket)
}

/**
 * Télécharge le billet comme image ou PDF
 * Essaie html2canvas si disponible, sinon fallback vers impression navigateur
 */
export const downloadTicketAsImage = async (ticket: Ticket): Promise<void> => {
    try {
        let html2canvas: any

        try {
            // @ts-ignore - dépendance optionnelle
            html2canvas = (await import('html2canvas')).default
        } catch {
            console.warn('html2canvas non installé. Utilisation de l\'approche native.')
            downloadTicketAsScreenshot(ticket)
            return
        }

        const ticketHTML = createTicketHTML(ticket)
        const tempDiv = document.createElement('div')
        tempDiv.innerHTML = ticketHTML
        tempDiv.style.position = 'absolute'
        tempDiv.style.left = '-9999px'
        tempDiv.style.width = '800px'
        document.body.appendChild(tempDiv)

        const canvas = await html2canvas(tempDiv, {
            backgroundColor: '#1D1E1C',
            scale: 2,
            logging: false,
        })

        const link = document.createElement('a')
        link.href = canvas.toDataURL('image/png')
        link.download = `billet-${ticket.ticketNumber}.png`
        link.click()

        document.body.removeChild(tempDiv)
    } catch (error) {
        console.error('Erreur lors du téléchargement du billet:', error)
        downloadTicketAsScreenshot(ticket)
    }
}

/**
 * Crée l'HTML de présentation du billet
 */
function createTicketHTML(ticket: Ticket): string {
    return `
    <div style="
      background: linear-gradient(135deg, #242624 0%, #2C2E2C 100%);
      border: 2px solid rgba(56, 227, 143, 0.3);
      border-radius: 16px;
      padding: 40px;
      width: 100%;
      color: #E9EEEC;
      font-family: 'Archivo', sans-serif;
    ">
      <!-- Header -->
      <div style="text-align: center; margin-bottom: 30px;">
        <div style="
          font-family: 'Archivo Black', sans-serif;
          font-size: 32px;
          font-weight: 900;
          color: #38E38F;
          text-transform: uppercase;
          letter-spacing: 2px;
          margin-bottom: 10px;
        ">Billet Numérique</div>
        <div style="
          font-size: 12px;
          color: #6B7A72;
          letter-spacing: 1px;
          text-transform: uppercase;
        ">${ticket.ticketType}</div>
      </div>

      <!-- Event Info -->
      <div style="margin-bottom: 30px; padding: 20px; background: rgba(51, 53, 51, 0.5); border-radius: 12px;">
        <div style="font-size: 24px; font-weight: bold; margin-bottom: 15px; color: #99D7B8;">
          ${ticket.eventTitle}
        </div>
        <table style="width: 100%; border-collapse: collapse;">
          <tr style="border-bottom: 1px solid rgba(153, 215, 184, 0.12); padding: 10px 0;">
            <td style="padding: 10px 0; color: #6B7A72; font-size: 12px; text-transform: uppercase;">Date</td>
            <td style="padding: 10px 0; text-align: right; font-weight: bold;">${ticket.eventDate}</td>
          </tr>
          <tr style="border-bottom: 1px solid rgba(153, 215, 184, 0.12); padding: 10px 0;">
            <td style="padding: 10px 0; color: #6B7A72; font-size: 12px; text-transform: uppercase;">Heure</td>
            <td style="padding: 10px 0; text-align: right; font-weight: bold;">${ticket.eventTime}</td>
          </tr>
          <tr style="border-bottom: 1px solid rgba(153, 215, 184, 0.12); padding: 10px 0;">
            <td style="padding: 10px 0; color: #6B7A72; font-size: 12px; text-transform: uppercase;">Lieu</td>
            <td style="padding: 10px 0; text-align: right; font-weight: bold;">${ticket.eventLocation}</td>
          </tr>
        </table>
      </div>

      <!-- Holder & QR -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px;">
        <div>
          <div style="font-size: 11px; color: #6B7A72; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Détenteur</div>
          <div style="font-size: 18px; font-weight: bold; color: #38E38F;">${ticket.holderName}</div>
        </div>
        <div style="text-align: center;">
          <img src="https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=${encodeURIComponent(ticket.qrCodeData)}" 
               style="width: 160px; height: 160px; border-radius: 8px; border: 2px solid rgba(56, 227, 143, 0.3);" />
        </div>
      </div>

      <!-- Ticket Details -->
      <div style="padding: 20px; background: rgba(51, 53, 51, 0.5); border-radius: 12px; border-top: 2px solid rgba(56, 227, 143, 0.2);">
        <table style="width: 100%; border-collapse: collapse;">
          <tr style="border-bottom: 1px solid rgba(153, 215, 184, 0.12);">
            <td style="padding: 10px 0; color: #6B7A72; font-size: 12px; text-transform: uppercase;">Catégorie</td>
            <td style="padding: 10px 0; text-align: right;">${ticket.eventCategory}</td>
          </tr>
          <tr style="border-bottom: 1px solid rgba(153, 215, 184, 0.12);">
            <td style="padding: 10px 0; color: #6B7A72; font-size: 12px; text-transform: uppercase;">Numéro Billet</td>
            <td style="padding: 10px 0; text-align: right; font-family: monospace; font-size: 13px; color: #38E38F;">${ticket.ticketNumber}</td>
          </tr>
          <tr>
            <td style="padding: 10px 0; color: #6B7A72; font-size: 12px; text-transform: uppercase;">Prix</td>
            <td style="padding: 10px 0; text-align: right; font-weight: bold; color: #38E38F;">${ticket.price.toFixed(2)} €</td>
          </tr>
        </table>
      </div>

      <!-- Footer -->
      <div style="text-align: center; margin-top: 30px; font-size: 11px; color: #6B7A72;">
        <div>Conservez ce billet pour accéder à l'événement</div>
        <div style="margin-top: 10px;">AtlaxOasis Events - ${new Date().toLocaleDateString('fr-FR')}</div>
      </div>
    </div>
  `
}

/**
 * Imprime le billet dans un nouvel onglet
 */
function downloadTicketAsScreenshot(ticket: Ticket): void {
    const html = createTicketHTML(ticket)
    const newWindow = window.open()
    if (newWindow) {
        newWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Billet - ${ticket.ticketNumber}</title>
        <style>
          body { margin: 20px; background: #1D1E1C; font-family: 'Archivo', sans-serif; }
          @media print { body { margin: 0; } }
        </style>
      </head>
      <body>
        ${html}
        <script>
          setTimeout(() => window.print(), 500);
        </script>
      </body>
      </html>
    `)
        newWindow.document.close()
    }
}