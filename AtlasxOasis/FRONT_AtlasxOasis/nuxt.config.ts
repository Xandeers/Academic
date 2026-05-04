export default defineNuxtConfig({
  devtools: { enabled: false },
  ssr: false,

  routeRules: {
    '/api/**': {
      proxy: 'http://192.168.75.76/api/**'
    },
  },

  nitro: {
    devProxy: {
      '/api': {
        target: 'http://192.168.75.76/api',
        changeOrigin: true,
        prependPath: true,
      }
    }
  },

  modules: ['@pinia/nuxt', '@nuxtjs/tailwindcss', '@nuxt/image'],

  css: ['assets/css/main.css'],

  dir: {
    pages: 'pages',
    layouts: 'layouts',
    middleware: 'middleware',
    plugins: 'plugins',
    public: 'public',
    assets: 'assets',
  },

  components: {
    dirs: [
      '~/components',
      '~/components/ui',
      '~/components/event',
      '~/components/booking',
      '~/components/dashboard',
      '~/components/layout',
    ],
  },

  imports: {
    dirs: [
      'composables',
      'stores',
      'utils',
    ],
  },

  app: {
    baseURL: '/',
    head: {
      title: 'AtlasXOasis',
      link: [
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:ital,wght@0,400;0,500;0,600;1,400&display=swap',
        },
      ],
    },
  },

  image: {
    quality: 80,
    format: ['webp']
  },
})