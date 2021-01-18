const production = process.env.NODE_ENV === 'production'

const app = (process.env.GAE_APPLICATION || '').split('~')
const appEngineURL = app.length === 2 ? `https://${app[1]}.appspot.com` : null

export default {
  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    htmlAttrs: { lang: 'en' },
    title: 'The COVID Memorial',
    meta: [
      { charset: 'utf-8' },
      {
        name: 'viewport',
        content: 'width=device-width, initial-scale=1, viewport-fit=cover',
      },
      {
        hid: 'description',
        name: 'description',
        content:
          'The COVID Memorial is a place to commemorate all those around the world who have sadly lost their lives due to the pandemic.',
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

  plugins: ['~/plugins/axios', { src: '~/plugins/vue-cropper', ssr: false }],

  components: true,

  buildModules: ['@nuxtjs/eslint-module'],

  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/style-resources',
    'nuxt-helmet',
    'nuxt-vue-select',
  ],

  helmet: {},

  render: {
    csp: {
      hashAlgorithm: 'sha256',
      policies: {
        'default-src': ["'none'"],
        'base-uri': ["'self'"],
        'font-src': ["'self'", 'https://fonts.gstatic.com'],
        'frame-ancestors': ["'self'"],
        'connect-src': ["'self'", 'blob:', 'https://corona-api.com'],
        'manifest-src': ["'self'"],
        'img-src': [
          "'self'",
          'data:',
          'blob:',
          'https://storage.googleapis.com',
        ],
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
    baseURL: production ? `${appEngineURL}/api/` : 'http://localhost:3000/api/',
    browserBaseURL: production ? '/api/' : 'http://localhost:3000/api/',
    proxy: !production, // enable proxy for development
    prefix: '/api/', // used only when proxy is enabled
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
    vendor: ['vue-cropperjs'],
  },

  server: {
    port: process.env.PORT || 3000, // default: 3000
    host: '0.0.0.0', // default: localhost,
    timing: false,
  },
}
