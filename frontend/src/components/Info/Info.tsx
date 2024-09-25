import { Button, Group, Space, Image, Text, Modal, ScrollArea } from "@mantine/core";
import { IconInfoCircle } from "@tabler/icons-react";
import classes from "./Info.module.css"
import { useDisclosure } from "@mantine/hooks";
import { GithubButton } from "../GithubButton/GithubButton";


export function Info() {
    const icon = <IconInfoCircle size={16} />;
    const [opened, { open, close }] = useDisclosure(false);


    return (
        <>
            <Button 
            className={classes.infoButton} 
            justify="center" 
            radius={"md"}
            leftSection={icon} 
            variant="filled"
            onClick={open}
            > Info
            </Button>

            <Modal opened={opened} onClose={close} 
            styles={{
                title: {fontWeight: 510, alignItems: "center", display: "flex"}
              }}
            scrollAreaComponent={ScrollArea.Autosize}
            overlayProps={{
                backgroundOpacity: 0.55,
                blur: 3,
              }}
            title={
                <Group justify="center" align={"center"}>
                <IconInfoCircle size={16} style={{ margin: 3 }}/>
                <Text fw={700}>Info / Support</Text>
                <GithubButton></GithubButton>
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
                <Space h="sm"/>
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
        </>
    )
}