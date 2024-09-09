import { MantineProvider } from '@mantine/core'
import { theme } from './theme'
import { HomePage } from './pages/Home.page'
import '@mantine/core/styles.css';
import '@mantine/charts/styles.css';

function App() {
  return (
    <MantineProvider theme={theme} >
      <HomePage />
    </MantineProvider>
  )
}

export default App
