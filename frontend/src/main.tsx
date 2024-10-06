import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'

// Import the PWA service worker registration
import { registerSW } from 'virtual:pwa-register';

// Register the service worker with immediate update
registerSW({ immediate: true });

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
