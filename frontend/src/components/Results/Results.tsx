import { Book } from "../../pages/Home.page";
import { Card, Container, Group, Image, Text, Button, SimpleGrid, SegmentedControl, Modal, Flex } from "@mantine/core";
import classes from "./Results.module.css"
import { useState } from "react";
import React from "react";
import { IconCircleCheck, IconCircleX } from "@tabler/icons-react";
import { bookSupportedLibraries } from "../../LibraryConstants";
import { useDisclosure } from "@mantine/hooks";

declare var $sleek: any | undefined;

type ResultsProps = {
  input: Book[];
  library: string;
};

type LibraryStatusRequest = {
  is_libby: Boolean,
  library: String,
  book: Book
}

type LibraryStatusResponse = {
  is_available: boolean
  msg: string
  link: string
}

function hideSleekButton() {
  if (typeof $sleek !== 'undefined' && $sleek.hideButton) {
    $sleek.hideButton();
  }
}

function showSleekButton() {
  if (typeof $sleek !== 'undefined' && $sleek.showButton) {
    $sleek.showButton();
  }
}


export function Results({ input, library }: ResultsProps) {

  // Define an array of states, one for each item in the input array
  const [values, setValues] = useState<string[]>(input.map(() => "Libby"));
  const [loading, setLoading] = useState<boolean[]>(input.map(() => false));

  const [showModal, setShowModalHandlers] = useDisclosure(false, {
    onOpen: () => hideSleekButton(),
    onClose: () => showSleekButton(),
  });
  const [modalContent, setModalContent] = useState<LibraryStatusResponse>(); // State for modal content


  function openNewWindow(link: string) {
    window.open(link, "_blank")
  }

  async function getLibraryStatus(request: LibraryStatusRequest, index: number) {
    // Set loading state for the corresponding index to true
    setLoading((prevLoading) => {
      const newLoading = [...prevLoading];
      newLoading[index] = true;
      return newLoading;
    });

    try {
      const res = await fetch("/libraryCheck", {
        method: 'POST',
        body: JSON.stringify(request),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      // Check if the response is ok, else throw an error
      if (!res.ok) {
        const errorData = await res.json(); // Parse error response
        throw new Error(errorData.error || 'Error checking library status');
      }

      // Process the successful response
      const data = await res.json();
      setModalContent(data);
      setShowModalHandlers.open();
      hideSleekButton();

    } catch (error) {
      // Handle the error (optional: surface error to UI or logs)
      console.error('Error fetching library status:', error);
      alert("Error: Unable to check library status. Please try again later.");
    } finally {
      // Set loading state for the corresponding index to false
      setLoading((prevLoading) => {
        const newLoading = [...prevLoading];
        newLoading[index] = false;
        return newLoading;
      });
    }
  }

  // Function to handle change in SegmentedControl for a specific index
  const handleSegmentedControlChange = (index: number, newValue: string) => {
    setValues((prevValues) => {
      const newValues = [...prevValues];
      newValues[index] = newValue;
      return newValues;
    });
  };

  const openModal = (book: Book, index: number) => {
    const currentValue = values[index];
    // need to check book support in case user switches between an unsupported library and back
    if (currentValue === "Libby" || !(library in bookSupportedLibraries) || currentValue === undefined) {
      // Perform action for Libby
      getLibraryStatus({ is_libby: true, library: library, book: book }, index)
    } else {
      getLibraryStatus({ is_libby: false, library: library, book: book }, index)
    }
  };

  const GreenCheckIcon = () => ( // TODO: Don't Hardcode Color, make it the var <mantine-green-5> for example
    <IconCircleCheck stroke={2} style={{ margin: 2 }} color={"#51cf66"} />
  );

  const RedCrossIcon = () => ( // TODO: Don't Hardcode Color, make it the var <mantine-red-8> for example
    <IconCircleX stroke={2} style={{ margin: 2 }} color={"#e03131"} />
  );

  return (
    <Container key={"resultsContainer"}>
      <SimpleGrid
        key={"simpleGrid"}
        type="container"
        cols={{ base: 1, '670px': 2 }}
        spacing={{ base: "xl", sm: 'xl' }}
      >
        {
          input.map((d, index) =>
          (
            <React.Fragment key={index + "fragment"}>
              <Card key={index + "card"} className={classes.card} shadow="md" padding="lg" radius="md" withBorder>
                <Card.Section key={index + "cardSection"}>
                  <Image
                    key={index + "img"}
                    src={d.image_link}
                    height={160}
                    fit="contain"
                  />
                </Card.Section>
                <Group key={index + "infoText"} justify="space-between" mt="md" mb="xs">
                  <Text key={index + "text1"} fw={600}>{d.title}</Text>
                  <Text key={index + "text2"} fw={250}>{d.author}</Text>
                </Group>

                <SegmentedControl
                  key={index + "segControl"}
                  data={[
                    {
                      value: "Libby",
                      label: "Libby",
                    },
                    {
                      value: "Book",
                      label: "Book",
                      disabled: !(library in bookSupportedLibraries)
                    },
                  ]}
                  radius="md"
                  value={
                    (library in bookSupportedLibraries) && values[index] !== undefined ? values[index] : "Libby"
                  }
                  onChange={(newValue) => handleSegmentedControlChange(index, newValue)}
                ></SegmentedControl>
                <br key={index + "br"}></br>

                <Group key={index + "btnGroup"} justify="space-around">
                  <Button
                    key={index + "grButton"}
                    color="blue"
                    radius="md"
                    onClick={(_e) => openNewWindow(d.link)}
                  >Goodreads Review</Button>
                  <Button
                    key={index + "libraryButton"}
                    color="blue"
                    radius="md"
                    onClick={(_e) => openModal(d, index)}
                    loading={loading[index]}
                    disabled={(library == "" || library == undefined)}
                  >Check Library</Button>
                </Group>
              </Card>
            </React.Fragment>
          )
          )}
      </SimpleGrid>
      <Modal
        styles={{
          title: { fontWeight: 510, alignItems: "center", display: "flex" }
        }}
        key={"modal"}
        title={
          <>
            Library Status
            {modalContent?.is_available ? <GreenCheckIcon /> : <RedCrossIcon />}
          </>
        }
        onClose={setShowModalHandlers.close}
        opened={showModal}
        size="md"
        centered
        overlayProps={{
          backgroundOpacity: 0.55,
          blur: 3,
        }}
      >
        <Text key={"modalText"} size="sm">{modalContent?.msg}</Text>
        <br></br>
        <Flex justify={"flex-end"}>
          <Button
            key={"libraryStatusBtn"}
            onClick={() => openNewWindow(modalContent?.link!!)}
          >Open Library Search</Button>
        </Flex>
      </Modal>
    </Container>
  )

}