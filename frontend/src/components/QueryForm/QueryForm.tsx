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

    const handleFormSubmit = () => {
        // Create a new URLSearchParams object
        const params = new URLSearchParams(searchParams);
    
        // Set the "gr_id" parameter to the link value
        params.set("gr_id", link);
    
        // Update the search parameters in the URL
        setSearchParams(params);
        
        // Call the onFormSubmit function with the updated request
        onFormSubmit({ num_books: 5, gr_url: link });
      };


    return (
        <>
        <input type="text" value={link} onChange={(e) => setLink(e.target.value)}></input>
        <button onClick={handleFormSubmit}>Get data</button>
        </>
    );
}