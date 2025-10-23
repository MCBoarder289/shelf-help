import { Button, Center, Container, SegmentedControl, Select, MultiSelect, Slider, TextInput, Stack, rem, LoadingOverlay, Box, Switch, Loader, Group } from "@mantine/core";
import classes from "./QueryForm.module.css"
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { bookRequest } from "../../pages/Home.page";
import { IconGripHorizontal, IconArrowsShuffle, IconSearch, IconRocketOff, IconRocket } from '@tabler/icons-react';
import { librarySelectValues } from "../../LibraryConstants";
import { Text } from '@mantine/core';


export function QueryForm({ 
    onFormSubmit = (_request: bookRequest) => { }, 
    loading, 
    librarySubmit = (_libraryName: String) => {},
    library,
    bookList,
}: { 
    onFormSubmit: (request: bookRequest) => void, 
    loading: boolean,  
    librarySubmit: (libraryName: string) => void,
    library: string,
    bookList: string[] | undefined,
}) {

    const [link, setLink] = useState("");
    const [errorStatus, setErrorStatus] = useState(false);
    const [searchParams, setSearchParams] = useSearchParams();
    const [numBooks, setNumBooks] = useState(4)
    const [searchMode, setSearchMode] = useState('shuffle')
    const [bookListSearch, setBookListSearch] = useState<string[] | null>(null)
    const [getAiRecs, setGetAiRecs] = useState(false)

    const AI_ENABLED = import.meta.env.VITE_AI_ENABLED === 'true';

    const aiMessages = [
        "Asking the AI for recommendations...",
        "Waiting for the AI to get you some new ideas...",
        "Analyzing your reading preferences...",
        "Searching the digital library universe...",
    ];

    const [currentMessage, setCurrentMessage] = useState(aiMessages[0]);

    useEffect(() => {
        let index = 0;
        const interval = setInterval(() => {
            index = (index + 1) % aiMessages.length; // Cycle through messages
            setCurrentMessage(aiMessages[index]);
        }, 6000); // Change message every 6 seconds

    return () => clearInterval(interval); // Cleanup on unmount
    }, []);

    const marks = [
        { value: 1, label: '1' },
        { value: 2, label: '2' },
        { value: 3, label: '3' },
        { value: 4, label: '4' },
      ];
      
    const shuffleIcon = <IconArrowsShuffle size={28} />
    const searchIcon = <IconSearch size={28} />

    // Initialize the link state with the value of the "gr_id" parameter from URL
    useEffect(() => {
        const grId = searchParams.get("gr_id");
        const libId = searchParams.get("lib_id");
        if (grId) {
            setLink(grId);
            localStorage.setItem("gr_id", grId)
        } else {
            if (localStorage.getItem("gr_id")) {
                setLink(localStorage.getItem("gr_id")!!)
            }
        }
        if (libId) {
            updateLibraryId(libId)
        } else {
            if (localStorage.getItem("lib_id")) {
                updateLibraryId(localStorage.getItem("lib_id")!!)
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

    function updateLibraryId(libraryId: string) {
        // never storing a blank library in local storage
        if (libraryId != null) { localStorage.setItem("lib_id", libraryId) }
        librarySubmit(libraryId)
    }

    const handleFormSubmit = () => {

        const validUrl = validateUrlInput()
        if (validUrl) {
            // Create a new URLSearchParams object
            const params = new URLSearchParams(searchParams);

            // Set the "gr_id" parameter to the link value
            params.set("gr_id", link);
            params.set("lib_id", library)

            // Update the search parameters in the URL
            setSearchParams(params);
            // Call the onFormSubmit function with the updated request
            const request = searchMode == 'shuffle' ? 
                { num_books: numBooks, gr_url: link, book_keys: null, get_ai_recs: getAiRecs } 
                : { num_books: 0, gr_url: link, book_keys: bookListSearch ? bookListSearch : null, get_ai_recs: getAiRecs }
            onFormSubmit(request);
        }
      };

      function searchSpecificBooks(bookList: string[]) {
        setBookListSearch(bookList)
        const validUrl = validateUrlInput()
        if (validUrl) {
            // Create a new URLSearchParams object
            const params = new URLSearchParams(searchParams);

            // Set the "gr_id" parameter to the link value
            params.set("gr_id", link);
            params.set("lib_id", library)

            // Update the search parameters in the URL
            setSearchParams(params);
            // no longer submitting simply when selecting on the dropdown
            // the ux implication is that we have to hit "Get Data" onces bookList is selected
            // onFormSubmit({num_books: 0, gr_url: link, book_keys: bookList, get_ai_recs: getAiRecs})
        }
      }

      function setSearchModeAndClearList(newSearchMode: string) {
        setSearchMode(newSearchMode)
        setBookListSearch([])
      }


    return (
        <Container size="md">
            <Stack>
            <TextInput
                    className={classes.input}
                    label="Goodreads Shelf URL"
                    placeholder="Enter Goodreads Shelf URL"
                    size="sm"
                    value={link}
                    error={errorStatus}
                    onChange={(e) => updateErrorAndLink(e)}
                ></TextInput>
            <Select
                className={classes.select}
                label="Select Library"
                data={librarySelectValues}
                placeholder="Search for library here..."
                value={library}
                limit={100}
                searchable
                onChange={(value, _option) => updateLibraryId(value!!)}
            ></Select>
            <SegmentedControl
            value={searchMode}
            data={[
              {
                value: "shuffle",
                label: (
                    <Center style={{ gap: 10 }}>
                        <IconArrowsShuffle></IconArrowsShuffle>
                        <span>Shuffle</span>
                    </Center>
                ),
              },
              {
                value: "search",
                label: (
                    <Center style={{ gap: 10 }}>
                        <IconSearch></IconSearch>
                        <span>Search</span>
                    </Center>
                ),
              }
            ]}
            onChange={setSearchModeAndClearList}
            ></SegmentedControl>
            <SegmentedControl
                value={getAiRecs ? 'true' : 'false'}
                data={[
                    { 
                        value: 'false', 
                        label: (
                            <Center style={{ gap: 10 }}>
                                <IconRocketOff></IconRocketOff>
                                <span>No AI</span>
                            </Center>
                        ) 
                    },
                    { 
                        value: 'true',
                        disabled: !AI_ENABLED,
                        label: (
                            <Center style={{ gap: 10 }}>
                                <IconRocket></IconRocket>
                                <span>AI Suggestions</span>
                            </Center>
                        ) 
                    },
                ]}
                onChange={(val) => setGetAiRecs(val === 'true')}
            ></SegmentedControl>
            {
                searchMode === 'shuffle' ? (
                    <>
                        <label className={"m_8fdc1311 mantine-InputWrapper-label mantine-TextInput-label"}>Number of Suggested Books</label>
                        <Slider
                            classNames={classes}
                            thumbChildren={
                                <IconGripHorizontal style={{ width: rem(20), height: rem(20) }} stroke={1.5} />
                            }
                            defaultValue={numBooks}
                            onChange={(value) => setNumBooks(value)}
                            min={1}
                            max={4}
                            marks={marks}
                        />
                        <br></br>
                    </>
                ) : (
                    <>
                        <Box pos="relative">
                        <LoadingOverlay visible={loading} loaderProps={{ children: ' ' }} />
                        <MultiSelect
                            label="Select Books"
                            placeholder="Search for books/authors.."
                            data={bookList}
                            maxValues={10}
                            disabled={bookList == undefined}
                            onChange={searchSpecificBooks}
                            nothingFoundMessage="Nothing found..."
                            comboboxProps={{ position: 'bottom', middlewares: { flip: false, shift: false } }}
                            searchable
                        />
                        </Box>
                    </>
                )
            }
            {
                getAiRecs && loading ? (
                    <>
                    <Group justify="center">
                         <Text className={classes.pulse}>
                            {currentMessage}
                            </Text>
                    </Group>
                    </>
                ) : null
            }
            </Stack>
            <br></br>
            <Button 
                className={classes.button}
                onClick={handleFormSubmit}
                loading={loading}
                leftSection={searchMode == 'shuffle' ? shuffleIcon : searchIcon}
                radius="md"
                fullWidth
                >Get Data</Button>
        </Container>
    );
}