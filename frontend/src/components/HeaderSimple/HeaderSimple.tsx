import { Container, Title, rem, useMantineTheme, Switch, useMantineColorScheme, Space, Burger, Menu, Group, Modal, ScrollArea, Text, Image, CloseButton } from '@mantine/core';
import classes from './HeaderSimple.module.css';
import icon from "/images/ios/256.png"
import { IconBrandGithub, IconBulb, IconCoffee, IconInfoCircle, IconMoonStars, IconSun } from '@tabler/icons-react';
import { useEffect } from 'react';
import { useDisclosure } from '@mantine/hooks';

declare var $sleek: any;

export function HeaderSimple() {

  const { colorScheme, toggleColorScheme } = useMantineColorScheme();
  const [burgerOpened, burgerHandlers] = useDisclosure();
  const [infoModalOpened, infoModalHandlers] = useDisclosure(false);
  const [supportModalOpened, supportModalHandlers] = useDisclosure(false);

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

  function openSleek() {
    $sleek.open()
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
    <>
      <Container size="md" className={classes.inner}>
        <div className={classes.inner}>
          <img src={icon} className={classes.headerlogo} />
          <Space w="sm" />
          <Title size="h2" className={classes.title}>
            Shelf Help
          </Title>
        </div>
        <div className={classes.inner}>
          <Switch size="md" color="dark.4" onLabel={sunIcon} offLabel={moonIcon} checked={colorScheme === 'dark' ? true : false} onChange={toggleColorSchemeAndTheme} />
          <Space w="md" />
          <Menu onClose={burgerHandlers.toggle} width={200} shadow="md">
            <Menu.Target>
              <Burger opened={burgerOpened} onClick={burgerHandlers.toggle} aria-label="Toggle navigation"></Burger>
            </Menu.Target>

            <Menu.Dropdown>
              <Menu.Item leftSection={<IconInfoCircle size={16} />} onClick={infoModalHandlers.open}>
                How to use
              </Menu.Item>
              <Menu.Item leftSection={<IconCoffee size={16} />} onClick={supportModalHandlers.open}>
                Buy me a coffee
              </Menu.Item>
              <Menu.Item leftSection={<IconBulb size={16} />} onClick={openSleek}>
                Give us feedback
              </Menu.Item>
              <Menu.Item leftSection={<IconBrandGithub size={16} />} onClick={() => window.open("https://github.com/MCBoarder289/shelf-help", "_blank")}>
                Source Code
              </Menu.Item>
            </Menu.Dropdown>
          </Menu>
        </div>
      </Container>
      {/* Info Modal */}
      <Modal opened={infoModalOpened} onClose={infoModalHandlers.close}
        styles={{
          title: { fontWeight: 510, alignItems: "center", display: "flex" }
        }}
        scrollAreaComponent={ScrollArea.Autosize}
        overlayProps={{
          backgroundOpacity: 0.55,
          blur: 3,
        }}
        title={
          <Group justify="center" align={"center"}>
            <IconInfoCircle size={16} style={{ margin: 3 }} />
            <Text fw={700}>How to use</Text>
          </Group>
        }>
        <Text>
          Shelf Help was designed to help you make a quick decision on what book should be next in your "to-read" shelf on Goodreads.
        </Text>
        <Space h="sm" />
        <Text fw={700}>Step 1: Insert a Goodreads shelf URL</Text>
        <Text>
          Simply copy the `Share` link from Goodreads and paste it into the input box.
        </Text>
        <Space h="sm" />
        <Text>
          Images below show you how to do this from the Goodreads app:
        </Text>
        <Group justify="center" grow>
          <Image
            src={"https://drive.google.com/thumbnail?id=1ScHB-yypcEf2gbH7vvuK1qMeLI3BasAX&sz=w1000"}
          />
          <Image
            src={"https://drive.google.com/thumbnail?id=1s2Zpgs6cWdWwK2js3jPqsdET9TWBlY0I&sz=w1000"}
          />
        </Group>
        <Space h="sm" />
        <Text fw={700}>Step 2: Select your library</Text>
        <Text>
          Depending on which library you select will dictate if you can search for physical books. Libby is available for all libraries listed.
        </Text>
        <Space h="sm" />
        <Text fw={700}>Step 3: Choose to Shuffle or Search</Text>
        <Text>
          In Shuffle mode, you can choose how many suggestions to receive. 4 is the max and the default.
        </Text>
        <Space h="sm" />
        <Text>
          In Search mode, you will be able to search for a Title/Author in the search bar after you click "Get Data"
        </Text>
        <Space h="sm" />
        <Text fw={700}>Step 4: Click Get Data</Text>
        <Text>
          Your shelf data is cached for 30 minutes. After that, any changes you make would be reflected.
        </Text>
        <Space h="sm" />
        <Text>
          Your Goodreads url and Library are saved and you can bookmark this link to skip steps 1 and 2 next time!
        </Text>
        <Space h="sm" />
        <Text fw={700}>Step 5: Check Goodreads Review or Library Availability</Text>
        <Text>
          The "Goodreads Review" button will take you to the Goodreads review page.
        </Text>
        <Space h="sm" />
        <Text>
          The "Check Library" button will see if it is available at your selected library.
        </Text>
        <Space h="sm" />
        <Text>
          Choosing "Book" will search for availability of a physical copy, whereas choosing "Libby" will search for Libby availability.
        </Text>
        <Space h="sm" />
        <Text fw={700}>Step 6: Repeat as needed!</Text>
        <Text>
          In shuffle mode, feel free to click "Get Data" multiple times and get new suggestions!
        </Text>
        <Space h="sm" />
        <Text>
          You can also change libraries or mediums at any time.
        </Text>
        <Space h="sm" />
      </Modal>
      {/* Buy me a coffee modal */}
      <Modal
        opened={supportModalOpened}
        onClose={supportModalHandlers.close}
        withCloseButton={false} // Disable default close button
        size="400px"
        overlayProps={{
          backgroundOpacity: 0.55,
          blur: 3,
        }}
        styles={{
          body: {
            padding: 0, // Remove default padding
            maxWidth: "400px",
            width: "100%",
            height: "90vh",
            borderRadius: "10px",
            display: "flex",
            justifyContent: "center",
            overflow: "hidden", // Prevent scrollbars
          },
        }}
      >
        <div
          style={{
            position: "relative",
            width: "100%",
            height: "100%",
            backgroundColor: "white",
            borderRadius: "10px",
            overflow: "hidden",
            display: "flex",
            justifyContent: "center",
          }}
        >
          <iframe
            src="https://www.buymeacoffee.com/widget/page/michaelchapman?description=support-me&color=%23FFDD00"
            title="Buy Me a Coffee"
            style={{
              width: "100%",
              height: "100%",
              border: "none",
              overflow: "hidden", // Prevent iframe scroll
            }}
            allow="payment"
          ></iframe>

          {/* Mantine Close Button */}
          <CloseButton
            onClick={supportModalHandlers.close}
            style={{
              position: "absolute",
              top: "10px",
              right: "10px",

            }}
          />
        </div>
      </Modal>
    </>
  );
}
