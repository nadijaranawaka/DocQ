import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],

  // Production build settings
  build: {
    outDir: 'dist',
    sourcemap: false,      // disable in production for security
    minify: 'esbuild',     // fast and efficient minification
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        // Split vendor libraries into separate chunks for better caching
        manualChunks: {
          vendor:   ['react', 'react-dom'],
          router:   ['react-router-dom'],
          supabase: ['@supabase/supabase-js'],
        },
      },
    },
  },

  // Dev server settings
  server: {
    port: 5173,
    strictPort: true,  // fail if port is taken instead of switching
  },

  // Preview server (npm run preview)
  preview: {
    port: 4173,
  },
})
