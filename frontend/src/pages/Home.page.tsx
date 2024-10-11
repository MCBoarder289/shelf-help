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

export type bookRequest = {num_books: number, gr_url: string, book_keys: string [] | null};


export function HomePage() {

  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<Book[]>([])
  const [bookList, setBookList] = useState<string[]|undefined>(undefined)
  const [library, setLibrary] = useState("")


  function getBookData(request: bookRequest) {
    setLoading(true);
    fetch("/bookChoices",  {
      method: 'POST',
      body: JSON.stringify(request),
      headers: {
    'Content-Type': 'application/json'
  }
    }).then(res => {
      if (!res.ok) {
          throw new Error('Failed to fetch data');
      }
      return res.json();
  })
  .then(data => {
      setData(data.books);
      setBookList(data.book_keys)
      setLoading(false);
  })
  .catch(error => {
      setLoading(false);
      console.error('Error fetching data:', error);
      alert("Error: This is likely due to a bad shelf url, empty shelf, or connection issue!")
  });
  }

  return (
    <AppShell header={{ height: 60, offset: false }} padding="md">
      <AppShell.Header className={classes.header_padding}>
        <HeaderSimple privacyPage={false} />
      </AppShell.Header>

      <AppShell.Main pt={`calc(${rem(60)} + var(--mantine-spacing-md))`}>
        <QueryForm onFormSubmit={getBookData} loading={loading} librarySubmit={setLibrary} library={library} bookList={bookList}></QueryForm>
        <br></br>
        <Results input={data} library={library}/>
      </AppShell.Main>
    </AppShell>
  );
}
