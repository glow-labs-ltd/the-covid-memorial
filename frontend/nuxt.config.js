const development = process.env.NODE_ENV !== 'production'

export default {
  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    htmlAttrs: { lang: 'en' },
    title: 'the-covid-memorial',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: 'The COVID Memorial',
      },
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        rel: 'stylesheet',
        href:
          'https://fonts.googleapis.com/css2?family=Lora:wght@400;700&display=swap',
      },
    ],
  },

  css: ['~assets/scss/vars.scss'],

  styleResources: {
    scss: ['./assets/scss/*.scss'],
  },

  plugins: ['~/plugins/axios'],

  components: true,

  buildModules: ['@nuxtjs/eslint-module'],

  modules: ['@nuxtjs/axios', '@nuxtjs/style-resources', 'nuxt-helmet'],

  helmet: {},

  render: {
    csp: {
      hashAlgorithm: 'sha256',
      policies: {
        'default-src': ["'none'"],
        'base-uri': ["'self'"],
        'font-src': ["'self'", 'https://fonts.gstatic.com'],
        'frame-ancestors': ["'self'"],
        'connect-src': ["'self'"],
        'manifest-src': ["'self'"],
        'img-src': ["'self'", 'data:'],
        'object-src': ["'none'"],
        'script-src': ["'self'"],
        'script-src-attr': ["'none'"],
        'style-src': [
          "'self'",
          "'unsafe-inline'",
          'https://fonts.googleapis.com',
        ],
        'block-all-mixed-content': [],
        // 'upgrade-insecure-requests': [],
      },
      addMeta: false,
    },
  },

  axios: {
    baseURL: development ? 'http://localhost:3000' : '',
    proxy: development,
    prefix: '/api/',
  },

  proxy: {
    '/api/': { target: 'http://localhost:8000' },
  },

  build: {
    postcss: {
      preset: {
        autoprefixer: {
          grid: true,
        },
      },
    },
  },

  server: {
    port: process.env.PORT || 3000, // default: 3000
    host: '0.0.0.0', // default: localhost,
    timing: false,
  },
}
