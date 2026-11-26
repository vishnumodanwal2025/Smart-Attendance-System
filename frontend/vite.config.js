import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': 'http://127.0.0.1:8000',
      '/auth': 'http://127.0.0.1:8000',
      '/register': 'http://127.0.0.1:8000',
      '/schedules': 'http://127.0.0.1:8000',
      '/sessions': 'http://127.0.0.1:8000',
      '/attendance': 'http://127.0.0.1:8000',
      '/users': 'http://127.0.0.1:8000',
    }
  }
})
