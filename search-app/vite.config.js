import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import path from 'path'

// Define __dirname for ES Modules to handle file paths correctly
const __dirname = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  // This matches your GitHub Pages URL structure
  base: '/financial-demo/search/',
  
  plugins: [
    vue(),
    vueDevTools(),
  ],

  // FORCE VITE TO BUNDLE THE CSS
  build: {
    // This prevents Vite from splitting CSS into separate files that might get missed
    cssCodeSplit: false, 
    // This ensures CSS is generated as a standard file, not embedded in JS
    assetsInlineLimit: 0, 
  },

  resolve: {
    alias: {
      // Standard Vue alias
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      
      // The "Secret Sauce" alias that points directly to the SearchStax theme
      // We point to the 'js' library because that is where the CSS files live
      '@searchstax-theme': path.resolve(
        __dirname, 
        'node_modules/@searchstax-inc/searchstudio-ux-js/dist/styles/mainTheme.css'
      )
    },
  },
})