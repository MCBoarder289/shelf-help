import { Book } from "@/pages/Home.page";

  
type ResultsProps = {
    input: Book[];
};


export function Results({input}: ResultsProps) {
    return (
        <ul>
        {
          input.map(d =>
            ( <>
              <li>Title: {d.title}, Author: {d.author} </li>
              <ul>
              <li>GR Link: {d.link}</li>
              </ul>
              </>
            )
          )}
      </ul>
    )
   
}