import { Book } from "@/pages/Home.page";
import { Card, Container, Group, Image, Text, Button, SimpleGrid, SegmentedControl, Modal, Flex} from "@mantine/core";
import classes from "./Results.module.css"
import { useState } from "react";
import React from "react";
import { IconCircleCheck, IconCircleX } from "@tabler/icons-react";
import { bookSupportedLibraries } from "@/LibraryConstants";


  
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


export function Results({input, library}: ResultsProps) {

  // Define an array of states, one for each item in the input array
  const [values, setValues] = useState<string[]>(input.map(() => "Libby"));
  const [loading, setLoading] = useState<boolean[]>(input.map(() => false));

  const [showModal, setShowModal] = useState(false); // State for controlling modal visibility
  const [modalContent, setModalContent] = useState<LibraryStatusResponse>(); // State for modal content


  function openNewWindow(link: string) {
    window.open(link, "_blank")
  }
  
  function getLibraryStatus(request: LibraryStatusRequest, index: number) {
    setLoading((prevLoading) => {
      const newLoading = [...prevLoading];
      newLoading[index] = true;
      return newLoading;
    });      
    
    fetch("/libraryCheck",  {
        method: 'POST',
        body: JSON.stringify(request),
        headers: {
      'Content-Type': 'application/json'
    }
      }).then(res => res.json()).then(data => {
        setModalContent(data)
        setShowModal(true)
      }).finally(
        () => {
          // Set loading state for the corresponding index to false when the request completes
          setLoading((prevLoading) => {
            const newLoading = [...prevLoading];
            newLoading[index] = false;
            return newLoading;
          });
        });
      
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
      getLibraryStatus({is_libby: true, library: library, book: book}, index)
    } else {
      getLibraryStatus({is_libby: false, library: library, book: book}, index)
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
          cols={{ base: 1, sm: 2 }}
          spacing={{ base: "xl", sm: 'xl' }}
        >
        {
          input.map((d, index) => 
          (
            <React.Fragment key={index+"fragment"}>
            <Card key={index+"card"} className={classes.card} shadow="md" padding="lg" radius="md" withBorder>
              <Card.Section key={index+"cardSection"}>
                <Image
                  key={index+"img"}
                  src={d.image_link}
                  height={160}
                  fit="contain"
                  />
              </Card.Section>
              <Group key={index+"infoText"} justify="space-between" mt="md" mb="xs">
                <Text key={index+"text1"} fw={600}>{d.title}</Text>
                <Text key={index+"text2"} fw={250}>{d.author}</Text>
              </Group>

              <SegmentedControl
                key={index+"segControl"}
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
                  (library in bookSupportedLibraries) && values[index] !== undefined ? values[index]  : "Libby"
                }
                onChange={(newValue) => handleSegmentedControlChange(index, newValue)}
              ></SegmentedControl>
              <br key={index+"br"}></br>

              <Group key={index+"btnGroup"} justify="space-around">
                <Button 
                  key={index+"grButton"}
                  color="blue"
                  radius="md" 
                  onClick={(_e) => openNewWindow(d.link)}
                  >Goodreads Review</Button>
                  <Button 
                  key={index+"libraryButton"}
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
            title: {fontWeight: 510, alignItems: "center", display: "flex"}
          }}
          key={"modal"}
          title={ 
              <>
              Library Status
              {modalContent?.is_available ? <GreenCheckIcon /> : <RedCrossIcon />}
              </>
          }
          onClose={() => setShowModal(false)}
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