/**
 * Génération d'un fichier .ics à partir des informations passées en paramètre.
 */

import type { Event } from "~/types/event";

const downloadICS = (icsContent: string): void => {
  const blob: Blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'event.ics');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}

export const generateICS = (event) => {
  if (!event) { return; }

  const formatICS = (timestamp: string) => {
    const date = timestamp.slice(0, 10).replaceAll('-', '');
    const hour = timestamp.slice(11, 16).replaceAll(':', '');
    return `${date}T${hour}00`;
  }

  const start = formatICS(event.begin_date);
  const end = formatICS(event.end_date);

  const icsContent = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'BEGIN:VEVENT',
    `DTSTART:${start}`,
    `DTEND:${end}`,
    `SUMMARY:${event.title}`,
    `DESCRIPTION:${event.description}`,
    `LOCATION:${event.location_id[0].name}`,
    'END:VEVENT',
    'END:VCALENDAR'
  ];

  downloadICS(icsContent.join('\r\n'));
}
