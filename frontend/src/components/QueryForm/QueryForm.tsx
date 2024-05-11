import { Button, Container, Flex, Group, Stack, TextInput } from "@mantine/core";
import classes from "./QueryForm.module.css"
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { bookRequest } from "@/pages/Home.page";


export function QueryForm({ onFormSubmit = (request: bookRequest) => { }, loading }: { onFormSubmit: (request: bookRequest) => void, loading: boolean }) {

    const [link, setLink] = useState("");
    const [errorStatus, setErrorStatus] = useState(false);
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
            setErrorStatus(true)
            // alert("URL must start with 'https://www.goodreads.com'")
            return false
        } else {
            return true
        }
    }

    function updateErrorAndLink(e: React.ChangeEvent<HTMLInputElement>) {
        setLink(e.target.value)
        if (errorStatus) {
            setErrorStatus(false)
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
                    placeholder="Enter Goodreads Shelf"
                    size="sm"
                    value={link}
                    error={errorStatus}
                    onChange={(e) => updateErrorAndLink(e)}
                ></TextInput>
            <Button 
                className={classes.button}
                onClick={handleFormSubmit}
                loading={loading}
                >Get data</Button>
            </Flex>
        </Container>
    );
}