import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './vitest.setup.mjs',
  },
  server: {
    proxy: {
      '/time': 'http://localhost:5000',
      '/libraryCheck': 'http://localhost:5000',
      '/bookChoices': 'http://localhost:5000',
    },
  },
});
