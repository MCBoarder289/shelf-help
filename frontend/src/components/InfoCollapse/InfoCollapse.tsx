import { Accordion, Button, Collapse, Container, Group, Space, Image, Text, Anchor } from "@mantine/core";
import { IconInfoCircle } from "@tabler/icons-react";
import classes from "./InfoCollapse.module.css"
import { useDisclosure } from "@mantine/hooks";


export function InfoCollapse() {
    const icon = <IconInfoCircle size={16} />;
    const [opened, { toggle }] = useDisclosure(false);


    return (
        <Container>
            <Button 
            className={classes.infoButton} 
            justify="center" 
            leftSection={icon} 
            variant="filled"
            onClick={toggle}
            > Info
            </Button>
            <br></br>
            <Collapse in={opened}>
                <br></br>
                <Accordion variant="contained" multiple={true}>
                    <Accordion.Item value="how-to">
                        <Accordion.Control>
                            How to Use
                        </Accordion.Control>
                        <Accordion.Panel>
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
                        <Text fw={700}>Step 2: Select Number of Suggestions</Text>
                        <Text>
                            You can select 1-4 suggestions with the provided slider (the default is 4).
                        </Text>
                        <Space h="sm" />
                        <Text fw={700}>Step 3: Click Get Data</Text>
                        <Text>
                            This app will then get all of your shelf data and pick a random subset for you.
                        </Text>
                        <Space h="sm" />
                            Your shelf data is cached for 30 minutes. After that, any changes you make would be reflected.
                        <Space h="sm" />
                        <Text fw={700}>Step 4: Check Goodreads Review or Library Availability</Text>
                        <Text>
                            The "Check Goodreads" button will take you to the Goodreads review page.
                        </Text>
                        <Text>
                            The "Check Library " button will see if it is available at your selected library.
                        </Text>
                        <Text>
                            Choosing "Book" will search for availability of a physical copy, whereas choosing "Libby" will serach for Libby availability.
                        </Text>
                        <Space h="sm" />
                        <Text fw={700}>Step 5: Repeat as needed!</Text>
                        <Text>
                            Feel free to click "Get Data" multiple times if you don't like the suggestions.
                        </Text>
                        <Text>
                            You can also change libraries or mediums at any time.
                        </Text>
                        <Space h="sm" />
                        <Anchor href="#">
                            Back to Top
                        </Anchor>
                        </Accordion.Panel>
                    </Accordion.Item>
                </Accordion>
            </Collapse>
            <br></br>
        </Container>
    )
}