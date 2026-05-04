/**
 * Renvoie une date à partir d'un timestamp
 * style :
 * - JJ/MM/AAAA : 'short'
 * - JJ mois AAAA : 'medium' (par défaut)
 * - jour JJ mois AAAA : 'full'
 * 
 */
export const getDateFromTimestamp = (
  timestamp: string,
  style: 'full' | 'medium' | 'short' = 'medium'
): string => { 
  if (!timestamp) { return ''; }
  
  const withoutTimeZone = timestamp.slice(0, 16);
  const date = new Date(withoutTimeZone);
  
  return new Intl.DateTimeFormat('fr-FR', { dateStyle: style}).format(date);
}

/**
 * Renvoie une heure à partir d'un timestamp en format HHhMM
 */
export const getHourFromTimestamp = (timestamp: string): string => {
  const hour: string = timestamp.slice(11, 16);

  if (!hour) { return '00h00'; }

  return hour.replace(":", "h");
}
