# AtlasXOasis — Groupe G14

Plateforme web de gestion et réservation d'événements développée dans le cadre du projet transversal MIF10 à l'Université Claude Bernard Lyon 1.

## Stack

- **NuxtJS 3** + TypeScript
- **Vue 3** Composition API
- **Pinia** — state management
- **TailwindCSS** — charte graphique custom
- **Lucide Vue** — icônes

## Lancer le projet

```bash
npm install
npm run dev
```

Ouvre [http://localhost:3000](http://localhost:3000)

## Charte graphique

| Rôle | Valeur |
|---|---|
| Texte | `#E9EEEC` |
| Background | `#1D1E1C` |
| Primary | `#99D7B8` |
| Secondary | `#218152` |
| Accent | `#38E38F` |
| Font titres | Archivo Black |
| Font corps | Archivo |

## Structure

```
components/    → composants UI, event, booking, dashboard
composables/   → logique métier réutilisable
layouts/       → default, auth, dashboard
middleware/    → guards de navigation
pages/         → routes automatiques NuxtJS
stores/        → état global Pinia
types/         → interfaces TypeScript
utils/         → fonctions utilitaires
```

> Voir la [Arborescence du projet](https://forge.univ-lyon1.fr/Mif10-G14-projet-transversal-2026/WebApp-AtlaxOasis-2026/-/wikis/Arborescence-du-projet) pour la documentation complète de l'arborescence.

## Équipe

| Membre | Périmètre |
|---|---|
| Sarah KESRAOUI | Parcours client — catalogue, réservation, profil, social |
| Leticia Ghilas | Parcours organisateur — dashboard, création, gestion |
|Raphael Heng | Fonctionnalités sociales — suivre, profil public, calendrier, événements des amis, responsive design
## Conventions Git

Commits : `type(scope): description — closes #N`

```
feat(auth): page login et register — closes #10 #11
feat(catalog): EventCard et EventFilters — closes #13 #14
fix(ui): correction AppModal sur mobile
chore(setup): installation TailwindCSS — closes #1
```

### Types de commits

| Type | Usage |
|---|---|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `chore` | Config, dépendances, setup |
| `style` | CSS, mise en page |
| `docs` | Documentation |

### Scopes

`ui` · `auth` · `catalog` · `booking` · `dashboard` · `social` · `api` · `setup` 