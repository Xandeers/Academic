/**
 * Formate un nombre au format français (ex: 1 250 000)
 */

export const formatFrenchNumber = (num: number | null | undefined): string => {
  if (num === undefined || num === null) {
    return '0';
  }

  return new Intl.NumberFormat('fr-FR').format(num);
}
