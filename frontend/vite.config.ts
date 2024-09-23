import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/libraryCheck': 'http://0.0.0.0:5000',
      '/bookChoices': 'http://0.0.0.0:5000',
    },
  },
})
