import React, { useEffect, useState } from 'react';
import { createTheme, MantineProvider } from '@mantine/core';
import { HeaderSimple } from './components/HeaderSimple';



const theme = createTheme({
  fontFamily: 'Open Sans, sans-serif',
  primaryColor: 'blue',
});

function App() {
  const [currentTime, setCurrentTime] = useState(0)

  useEffect(() => {
    // fetch('/time').then(res => res.json()).then(data => {
    //   setCurrentTime(data.time)
    // })
  }, []
  )

  return (
    <MantineProvider>
      <HeaderSimple/>
    </MantineProvider>
  );
}

export default App;
