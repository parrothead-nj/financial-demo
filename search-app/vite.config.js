import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import path from 'path' // Added this import

// Define __dirname for ES Modules
const __dirname = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  base: '/financial-demo/search/',
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      // Points directly to the SearchStax theme in your node_modules
      '@searchstax-theme': path.resolve(__dirname, 'node_modules/@searchstax-inc/searchstudio-ux-vue/dist/styles/mainTheme.css')
    },
  },
})