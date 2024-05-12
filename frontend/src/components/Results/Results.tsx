import { Book } from "@/pages/Home.page";
import { Card, Container, Group, Image, Text, Button, Badge, Stack, SimpleGrid, SegmentedControl, Modal} from "@mantine/core";
import classes from "./Results.module.css"
import { useState } from "react";


  
type ResultsProps = {
    input: Book[];
    library: string;
};

type LibraryStatusRequest = {
  is_libby: Boolean,
  library: String,
  book: Book
}

function openNewWindow(link: string) {
  window.open(link, "_blank")
}


export function Results({input}: ResultsProps) {

  // Define an array of states, one for each item in the input array
  const [values, setValues] = useState<string[]>(input.map(() => "Book"));
  const [showModal, setShowModal] = useState(false); // State for controlling modal visibility
  const [modalContent, setModalContent] = useState(""); // State for modal content

  // Function to handle change in SegmentedControl for a specific index
  const handleSegmentedControlChange = (index: number, newValue: string) => {
    setValues((prevValues) => {
      const newValues = [...prevValues];
      newValues[index] = newValue;
      return newValues;
    });
  };

  const openModal = (link: string, index: number) => {
    const currentValue = values[index];
    if (currentValue === "Libby") {
      // Perform action for Libby
      setModalContent(`Performing action for Libby with link: ${link}`);
      setShowModal(true);
      // Here you can make API calls or perform other actions specific to Libby
    } else {
      // Perform action for Book
      // Here you can perform any action specific to Book, if needed
    }
  };

    return (
      <Container>
        <SimpleGrid 
          cols={{ base: 1, sm: 2 }}
          spacing={{ base: "xl", sm: 'xl' }}
        >
        {
          input.map((d, index) => 
          (
            <>
            <Card key={index} className={classes.card} shadow="md" padding="lg" radius="md" withBorder>
              <Card.Section>
                <Image
                  src={d.image_link}
                  height={160}
                  fit="contain"
                  />
              </Card.Section>
              <Group justify="space-between" mt="md" mb="xs">
                <Text fw={600}>{d.title}</Text>
                <Text fw={250}>{d.author}</Text>
              </Group>

              <SegmentedControl 
                data={["Book", "Libby"]}
                radius="md"
                value={values[index]}
                onChange={(newValue) => handleSegmentedControlChange(index, newValue)}
              ></SegmentedControl>
              <br></br>

              <Group justify="space-around">
                <Button 
                  color="blue"
                  radius="md" 
                  onClick={(_e) => openNewWindow(d.link)}
                  >Check Goodreads</Button>
                  <Button 
                  color="blue"
                  radius="md" 
                  onClick={(_e) => openModal(d.link, index)}
                  >Check Library</Button>
                </Group>
            </Card>
            </>
          )
        )}
        </SimpleGrid>
        <Modal
          title="Library Modal"
          onClose={() => setShowModal(false)}
          opened={showModal}
          size="sm"
         >
          <Text>{modalContent}</Text>
          <Button onClick={() => setShowModal(false)}>Close</Button>
        </Modal>
      </Container>
    )
   
}