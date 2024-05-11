import { Button, Container, Flex, Group, Stack, TextInput } from "@mantine/core";
import classes from "./QueryForm.module.css"
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

type bookRequest = {num_books: number, gr_url: string};


export function QueryForm({onFormSubmit  = (request: bookRequest) => {}}) {

    const [link, setLink] = useState("");
    const [searchParams, setSearchParams] = useSearchParams();

    // Initialize the link state with the value of the "gr_id" parameter from URL
    useEffect(() => {
        const grId = searchParams.get("gr_id");
        if (grId) {
            setLink(grId);
        }
    }, [searchParams]);

    function validateUrlInput() {
        if(!link.startsWith("https://www.goodreads.com")) {
            alert("URL must start with 'https://www.goodreads.com'")
            return false
        } else {
            return true
        }
    }

    const handleFormSubmit = () => {

        const validUrl = validateUrlInput()
        if (validUrl) {
            // Create a new URLSearchParams object
            const params = new URLSearchParams(searchParams);

            // Set the "gr_id" parameter to the link value
            params.set("gr_id", link);

            // Update the search parameters in the URL
            setSearchParams(params);

            // Call the onFormSubmit function with the updated request
            onFormSubmit({ num_books: 5, gr_url: link });
        }
      };


    return (
        <Container size="md">
            <Flex justify="Flex-start" align="Flex-end" gap="md">
                <TextInput
                    className={classes.input}
                    label="Shelf Url"
                    placeholder="Enter Goodreads Shelf URL"
                    size="sm"
                    value={link}
                    // onChange={(e) => setLink(e.target.value)}
                ></TextInput>
            <Button 
                className={classes.button}
                onClick={handleFormSubmit}
                >Get data</Button>
            </Flex>
        </Container>
    );
}