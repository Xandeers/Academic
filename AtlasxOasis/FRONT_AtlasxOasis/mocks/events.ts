import type { Event } from '~/types/event';

export const eventTests: Event[] = [
  {
    id: '1',
    title: 'Soirée phonk tibétaine',
    description: 'Une soirée électro immersive au cœur de Lyon.',
    category: 'Musique',
    status: 'full',
    date: '2026-06-12', 
    time: '22h00',
    location: 'Lyon',
    price: 20,
    capacity: 100,
    reserved: 100,
    organizer: {
      id: '1',
      name: 'DJ Collective Lyon',
      certified: false,
      followersCount: 10000
    },
    tags: [{ id: '1', label: 'Musique' }, { id: '2', label: 'Électro' }],
    likesCount: 10000,
    createdAt: '2026-01-01'
  },
  {
    id: '2',
    title: 'Tournoi Among Us',
    description: 'Devenez le meilleur imposteur',
    category: 'E-Sport',
    status: 'published',
    date: '2026-06-15', 
    time: '18h30',
    location: 'Bordeaux',
    price: 45,
    capacity: 20,
    reserved: 5,
    organizer: {
      id: '2',
      name: 'Art & Co',
      certified: true,
      followersCount: 2500
    },
    tags: [{ id: '3', label: 'Atelier' }, { id: '4', label: 'Vin' }],
    likesCount: 450,
    createdAt: '2026-02-10'
  },
  {
    id: '3',
    title: 'Conférence Tech 2026',
    description: 'Le futur de l’IA et du développement Web.',
    category: 'Ateliers',
    status: 'draft',
    date: '2026-07-20', 
    time: '09h00',
    location: 'Paris',
    price: 0,
    capacity: 500,
    reserved: 320,
    organizer: {
      id: '3',
      name: 'TechHub',
      certified: true,
      followersCount: 50000
    },
    tags: [{ id: '5', label: 'IA' }, { id: '6', label: 'Web' }],
    likesCount: 8900,
    createdAt: '2026-03-01'
  },
  {
    id: '4',
    title: 'Yoga au Parc',
    description: 'Session matinale de Yoga Vinyasa pour tous les niveaux.',
    category: 'Sport',
    status: 'published',
    date: '2026-06-05', 
    time: '08h00',
    location: 'Marseille',
    price: 10,
    capacity: 30,
    reserved: 28,
    organizer: {
      id: '4',
      name: 'Zen Group',
      certified: false,
      followersCount: 800
    },
    tags: [{ id: '7', label: 'Bien-être' }],
    likesCount: 120,
    createdAt: '2026-03-15'
  },
  {
    id: '5',
    title: 'Festival Gastronomique',
    description: 'Venez goûter aux spécialités des meilleurs chefs de la région.',
    category: 'Ateliers',
    status: 'full',
    date: '2026-08-10', 
    time: '12h00',
    location: 'Lille',
    price: 15,
    capacity: 200,
    reserved: 200,
    organizer: {
      id: '5',
      name: 'Saveurs de France',
      certified: true,
      followersCount: 15000
    },
    tags: [{ id: '8', label: 'Food' }, { id: '9', label: 'Festival' }],
    likesCount: 3400,
    createdAt: '2026-03-20'
  },
  {
    id: '6',
    title: 'Randonnée Nocturne',
    description: 'Une marche de 10km sous les étoiles avec guide.',
    category: 'Sport',
    status: 'published',
    date: '2026-06-22', 
    time: '21h00',
    location: 'Grenoble',
    price: 5,
    capacity: 50,
    reserved: 12,
    organizer: {
      id: '6',
      name: 'Mountain Peak',
      certified: false,
      followersCount: 3200
    },
    tags: [{ id: '10', label: 'Nature' }],
    likesCount: 670,
    createdAt: '2026-03-22'
  },
  {
    id: '7',
    title: 'Vernissage Art Moderne',
    description: 'Exposition exclusive de jeunes talents locaux.',
    category: 'Culture',
    status: 'published',
    date: '2026-06-30', 
    time: '19h00',
    location: 'Nantes',
    price: 0,
    capacity: 80,
    reserved: 45,
    organizer: {
      id: '7',
      name: 'Galerie Futur',
      certified: true,
      followersCount: 1200
    },
    tags: [{ id: '11', label: 'Culture' }],
    likesCount: 310,
    createdAt: '2026-03-23'
  },
  {
    id: '8',
    title: 'Stand-up Comedy Club',
    description: '1h30 de rire avec 5 humoristes différents.',
    category: 'Culture',
    status: 'cancelled',
    date: '2026-07-14', 
    time: '20h30',
    location: 'Montpellier',
    price: 25,
    capacity: 60,
    reserved: 58,
    organizer: {
      id: '8',
      name: 'Rire & Co',
      certified: false,
      followersCount: 4500
    },
    tags: [{ id: '12', label: 'Humour' }],
    likesCount: 1500,
    createdAt: '2026-03-24'
  }
];

export const eventTest: Event = {
  id: '1',
  title: 'Événement test',
  description: 'Test description',
  category: 'Musique',
  status: 'full',
  date: '2026-06-12',
  time: '22h00',
  location: 'Lyon',
  price: 20,
  capacity: 100,
  reserved: 10,
  organizer: {
    id: '1',
    name: 'DJ Collective Lyon',
    certified: false,
    followersCount: 10_000
  },
  tags: [
    {
      id: '1',
      label: 'Musique'
    }
  ],
  likesCount: 10_000,
  createdAt: 'Toto'
};