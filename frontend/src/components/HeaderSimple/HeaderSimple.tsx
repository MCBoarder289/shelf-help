import { Container, Title, rem, useMantineTheme, Switch, useMantineColorScheme } from '@mantine/core';
import classes from './HeaderSimple.module.css';
import icon from "/images/icon.png"
import { IconMoonStars, IconSun } from '@tabler/icons-react';


export function HeaderSimple() {
 
  const {colorScheme, toggleColorScheme} = useMantineColorScheme();

  function toggleColorSchemeAndMeta() {
    if (colorScheme == 'dark') {
      document.querySelector("html")?.setAttribute("background-color", "#ffffff")
    }
    else if (colorScheme == 'light') {
      document.querySelector("html")?.setAttribute("background-color", "#242424")
    }
    toggleColorScheme()
  }


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
        <Title className={classes.title}>
          Shelf Help
        </Title>
        <Switch size="md" color="dark.4" onLabel={sunIcon} offLabel={moonIcon} checked={colorScheme === 'dark' ? true : false} onChange={toggleColorSchemeAndMeta} />
      </Container>
  );
}
