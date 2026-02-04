import '@searchstax-theme'
import { createApp } from 'vue'
import App from './App.vue'

// This MUST be a direct import to be bundled
import '../node_modules/@searchstax-inc/searchstudio-ux-js/dist/styles/mainTheme.css'

createApp(App).mount('#app')