import { Container, Title, rem, useMantineTheme, Switch, useMantineColorScheme } from '@mantine/core';
import classes from './HeaderSimple.module.css';
import icon from "/images/icon.png"
import { IconMoonStars, IconSun } from '@tabler/icons-react';
import { useEffect } from 'react';


export function HeaderSimple() {
 
  const {colorScheme, toggleColorScheme} = useMantineColorScheme();

  // Function to dynamically update the theme color in the meta tag
  const updateStatusBarColor = (theme: 'light' | 'dark') => {
    const themeColor = theme === 'dark' ? '#242424' : '#ffffff';
    const metaTag = document.querySelector('meta[name="theme-color"]');

    if (metaTag) {
      metaTag.setAttribute('content', themeColor);
    }
  };

  function toggleColorSchemeAndTheme() {
    toggleColorScheme()
    const metaTag = document.querySelector('meta[name="theme-color"]');
      if (metaTag) {
        if (colorScheme === 'dark') {
          metaTag.setAttribute('content', '#ffffff'); // Turn it back to white
        } else {
          metaTag.setAttribute('content', '#242424'); // Turn it back to dark
        }
      }
    }

      // On initial render, check the current theme and set the meta tag color accordingly
  useEffect(() => {
    const theme = colorScheme === 'dark' ? 'dark' : 'light';
    updateStatusBarColor(theme);
  }, []);

  const theme = useMantineTheme();

  const sunIcon = (
    <IconSun
      style={{ width: rem(16), height: rem(16) }}
      stroke={2.5}
      color={theme.colors.yellow[4]}
    />
  );

  const moonIcon = (
    <IconMoonStars
      style={{ width: rem(16), height: rem(16) }}
      stroke={2.5}
      color={theme.colors.blue[6]}
    />
  );

  return (
      <Container size="md" className={classes.inner}>
        <img src={icon} className={classes.headerlogo}/>
        <Title className={classes.title} style={{"--title-fw": "var(--mantine-h1-font-weight)", "--title-lh": "var(--mantine-h1-line-height)", "--title-fz": "var(--mantine-h2-font-size)"}}>
          Shelf Help Analytics
        </Title>
        <Switch size="md" color="dark.4" onLabel={sunIcon} offLabel={moonIcon} checked={colorScheme === 'dark' ? true : false} onChange={toggleColorSchemeAndTheme} />
      </Container>
  );
}
