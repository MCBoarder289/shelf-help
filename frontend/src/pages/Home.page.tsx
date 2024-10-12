import { HeaderSimple } from '../components/HeaderSimple/HeaderSimple';
import { AppShell, rem } from '@mantine/core';
import { useState } from 'react';
import { QueryForm } from '../components/QueryForm/QueryForm';
import { Results } from '../components/Results/Results';
import classes from './Home.module.css'

export type Book = {
  title: string,
  author: string,
  isbn: string,
  avg_rating: number,
  date_added: string,
  link: string,
  searchable_title: string,
  image_link: string,
  goodreads_id: string,

};

export type bookRequest = { num_books: number, gr_url: string, book_keys: string[] | null };


export function HomePage() {

  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<Book[]>([])
  const [bookList, setBookList] = useState<string[] | undefined>(undefined)
  const [library, setLibrary] = useState("")


  async function getBookData(request: bookRequest) {
    setLoading(true);

    try {
      const res = await fetch("/bookChoices", {
        method: 'POST',
        body: JSON.stringify(request),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      // Check for non-OK response status
      if (!res.ok) {
        const errorData = await res.json(); // Parse the response JSON
        throw new Error(errorData.error || 'Error: This is likely due to a bad shelf URL, empty shelf, or connection issue!"');
      }

      // Process successful response
      const data = await res.json();
      setData(data.books);
      setBookList(data.book_keys);

    } catch (error) {
      // Handle errors from both network issues and API response
      console.error('Error fetching data:', error);
      if(error == 'SyntaxError: Unexpected end of JSON input') {
        alert('Error: This is likely due to a bad shelf URL, empty shelf, or connection issue!')
      } else {
        alert(`${error}`);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell header={{ height: 60, offset: false }} padding="md">
      <AppShell.Header className={classes.header_padding}>
        <HeaderSimple privacyPage={false} />
      </AppShell.Header>

      <AppShell.Main pt={`calc(${rem(60)} + var(--mantine-spacing-md))`}>
        <QueryForm onFormSubmit={getBookData} loading={loading} librarySubmit={setLibrary} library={library} bookList={bookList}></QueryForm>
        <br></br>
        <Results input={data} library={library} />
      </AppShell.Main>
    </AppShell>
  );
}
