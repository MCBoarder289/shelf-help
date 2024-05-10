import { useState } from "react";

type bookRequest = {num_books: number, gr_url: string};


export function QueryForm({onFormSubmit  = (request: bookRequest) => {}}) {

    const [link, setLink] = useState("");




    return (
        <>
        <input type="text" value={link} onChange={(e) => setLink(e.target.value)}></input>
        <button onClick={() => onFormSubmit({num_books: 5, gr_url: link})}>Get data</button>
        </>
    );
}