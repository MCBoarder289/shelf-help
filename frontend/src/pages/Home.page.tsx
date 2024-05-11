import { HeaderSimple } from '@/components/HeaderSimple/HeaderSimple';
import { AppShell, rem } from '@mantine/core';
import { useState } from 'react';
import { QueryForm } from '@/components/QueryForm/QueryForm';
import { Results } from '@/components/Results/Results';

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

export type bookRequest = {num_books: number, gr_url: string};


export function HomePage() {
  const [currentTime, setCurrentTime] = useState(0);

  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<Book[]>([])

  function getTime() {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }


  function getBookData(request: bookRequest) {
    setLoading(true);
    fetch("/bookChoices",  {
      method: 'POST',
      body: JSON.stringify(request),
      headers: {
    'Content-Type': 'application/json'
  }
    }).then(res => res.json()).then(data => {
      setData(data.books)
      setLoading(false)
    });
  }

  return (
    <AppShell header={{ height: 60, offset: false }} padding="md">
      <AppShell.Header>
        <HeaderSimple />
      </AppShell.Header>

      <AppShell.Main pt={`calc(${rem(60)} + var(--mantine-spacing-md))`}>
      <button onClick={getTime}>Time Test</button>
      <p>The current time is {currentTime}</p>
      <br></br>
      <QueryForm onFormSubmit={getBookData} loading={loading}></QueryForm>
      <Results input={data} />
      </AppShell.Main>
    </AppShell>
  );
}
