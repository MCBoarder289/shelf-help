import { MantineProvider } from '@mantine/core'
import { theme } from './theme'
import { Router } from './Router';
import '@mantine/core/styles.css';

function App() {
  return (
    <MantineProvider theme={theme} >
      <Router />
    </MantineProvider>
  )
}

export default App
