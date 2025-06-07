import { createApp } from 'vue'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import App from './App.vue'

const vuetify = createVuetify({
    components,
    directives,
    theme: {
      themes: {
        light: {
          colors: {
            primary: '#4CAF50',
            secondary: '#1c84d9',
          },
        },
      },
    },
  })
  
createApp(App).use(vuetify).mount('#app')
