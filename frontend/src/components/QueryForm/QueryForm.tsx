import { Button, Container, Flex, Select, Slider, TextInput, Stack, rem } from "@mantine/core";
import classes from "./QueryForm.module.css"
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { bookRequest } from "@/pages/Home.page";
import { IconGripHorizontal } from '@tabler/icons-react';
import { librarySelectValues } from "../../LibraryConstants";


export function QueryForm({ 
    onFormSubmit = (_request: bookRequest) => { }, 
    loading, 
    librarySubmit = (_libraryName: String) => {},
}: { 
    onFormSubmit: (request: bookRequest) => void, 
    loading: boolean,  
    librarySubmit: (libraryName: string) => void,
}) {

    const [link, setLink] = useState("");
    const [errorStatus, setErrorStatus] = useState(false);
    const [searchParams, setSearchParams] = useSearchParams();
    const [numBooks, setNumBooks] = useState(4)


    const marks = [
        { value: 1, label: '1' },
        { value: 2, label: '2' },
        { value: 3, label: '3' },
        { value: 4, label: '4' },
      ];
      

    // Initialize the link state with the value of the "gr_id" parameter from URL
    useEffect(() => {
        const grId = searchParams.get("gr_id");
        if (grId) {
            setLink(grId);
            localStorage.setItem("gr_id", grId)
        } else {
            if (localStorage.getItem("gr_id")) {
                setLink(localStorage.getItem("gr_id")!!)
            }
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
        localStorage.setItem("gr_id", e.target.value)
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
            onFormSubmit({ num_books: numBooks, gr_url: link });
        }
      };


    return (
        <Container size="md">
            <Stack>
            <TextInput
                    className={classes.input}
                    label="Shelf URL"
                    placeholder="Enter Goodreads Shelf URL"
                    size="sm"
                    value={link}
                    error={errorStatus}
                    onChange={(e) => updateErrorAndLink(e)}
                ></TextInput>
            <label className={"m_8fdc1311 mantine-InputWrapper-label mantine-TextInput-label"}>Number of Suggested Books</label>
            <Slider
                classNames={classes}
                thumbChildren={
                    <IconGripHorizontal style={{ width: rem(20), height: rem(20) }} stroke={1.5} />
                }
                defaultValue={4}
                onChange={(value) => setNumBooks(value)}
                min={1}
                max={4}
                marks={marks}
            />
            </Stack>
            <br></br>
            <Flex justify="Flex-start" align="Flex-end" gap="md">
            <Select
                className={classes.select}
                label="Select Library"
                data={librarySelectValues}
                placeholder="Search for your library here..."
                limit={10}
                searchable
                onChange={(value, _option) => librarySubmit(value!!)}
            ></Select>
            <Button 
                className={classes.button}
                onClick={handleFormSubmit}
                loading={loading}
                radius="md"
                >Get Data</Button>
            </Flex>
        </Container>
    );
}