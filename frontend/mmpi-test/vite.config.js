import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: [
        'src/img/*',
        'src/fonts/Montserrat/*'
      ],
      manifest: {
        name: 'MMPI Test',
        short_name: 'MMPI',
        start_url: '/',
        display: 'standalone',
        background_color: '#ffffff',
        theme_color: '#4A90E2',
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,woff2,png,jpg,jpeg,svg}'],
        maximumFileSizeToCacheInBytes: 20 * 1024 * 1024,
        runtimeCaching: [
          {
            urlPattern: ({ request }) => request.destination === 'image',
            handler: 'CacheFirst',
            options: {
              cacheName: 'images-cache',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24 * 30, 
              },
            },
          },
          {
            urlPattern: ({ request }) => request.destination === 'font',
            handler: 'CacheFirst',
            options: {
              cacheName: 'fonts-cache',
              expiration: {
                maxEntries: 20,
                maxAgeSeconds: 60 * 60 * 24 * 365,
              },
            },
          },
        ],
      },
    }),
  ],
  server: {
    open: true,
    host: '0.0.0.0',
  },
});
