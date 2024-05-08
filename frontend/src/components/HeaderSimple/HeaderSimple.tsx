import { useState } from 'react';
import { Container, Group, Burger, Title, rem, useMantineTheme, Switch, useMantineColorScheme } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import classes from './HeaderSimple.module.css';
import icon from "../../public/images/icon.png"
import { IconMoonStars, IconSun } from '@tabler/icons-react';

const links = [
  { link: '/about', label: 'Features' },
  { link: '/pricing', label: 'Pricing' },
  { link: '/learn', label: 'Learn' },
  { link: '/community', label: 'Community' },
];



export function HeaderSimple() {
  const [opened, { toggle }] = useDisclosure(false);
  const [active, setActive] = useState(links[0].link);
  const {colorScheme, toggleColorScheme} = useMantineColorScheme();


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

  const items = links.map((link) => (
    <a
      key={link.label}
      href={link.link}
      className={classes.link}
      data-active={active === link.link || undefined}
      onClick={(event) => {
        event.preventDefault();
        setActive(link.link);
      }}
    >
      {link.label}
    </a>
  ));

  return (
    <header className={classes.header}>
      <Container size="md" className={classes.inner}>
        <img src={icon} className={classes.headerlogo}/>
        <Title className={classes.title}>
          Shelf Help
        </Title>
        <Group gap={5} visibleFrom="xs">
          {items}
        </Group>
        <Switch size="md" color="dark.4" onLabel={sunIcon} offLabel={moonIcon} checked={colorScheme === 'dark' ? true : false} onChange={toggleColorScheme} />
        <Burger opened={opened} onClick={toggle} size="sm" />
      </Container>
    </header>
  );
}
