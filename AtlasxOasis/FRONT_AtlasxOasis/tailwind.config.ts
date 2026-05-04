import type { Config } from 'tailwindcss'

export default {
  content: [
    './components/**/*.{vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './app.vue',
  ],
  theme: {
    extend: {
      colors: {
        bg:        '#1D1E1C',
        s1:        '#242624',
        s2:        '#2C2E2C',
        s3:        '#333533',
        primary:   '#99D7B8',
        secondary: '#218152',
        accent:    '#38E38F',
        muted:     '#6B7A72',
        muted2:    '#4A5450',
      },
      fontFamily: {
        title: ['Archivo Black', 'sans-serif'],
        body:  ['Archivo', 'sans-serif'],
      },
      borderColor: {
        DEFAULT: 'rgba(153, 215, 184, 0.12)',
        strong:  'rgba(153, 215, 184, 0.22)',
      },
    },
  },
} satisfies Config