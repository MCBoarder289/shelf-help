import { Welcome } from '../components/Welcome/Welcome';
import { ColorSchemeToggle } from '../components/ColorSchemeToggle/ColorSchemeToggle';
import { HeaderSimple } from '@/components/HeaderSimple/HeaderSimple';
import { AppShell, Text, rem } from '@mantine/core';
import { useHeadroom } from '@mantine/hooks';
import { useEffect, useState } from 'react';
import { QueryForm } from '@/components/QueryForm/QueryForm';

const lorem =
  'Lorem ipsum dolor sit amet consectetur adipisicing elit. Eos ullam, ex cum repellat alias ea nemo. Ducimus ex nesciunt hic ad saepe molestiae nobis necessitatibus laboriosam officia, reprehenderit, earum fugiat?';


export function HomePage() {
  const [currentTime, setCurrentTime] = useState(0);

  const [data, setData] = useState<Book[]>([])

  type Book = {
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


  function getTime() {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }

  type bookRequest = {num_books: number, gr_url: string};

  function getBookData(request: bookRequest) {
    fetch("/bookChoices",  {
      method: 'POST',
      body: JSON.stringify(request),
      headers: {
    'Content-Type': 'application/json'
  }
    }).then(res => res.json()).then(data => {
      setData(data.books)
    });
  }

  // useEffect(() => {
  //   setTimeout(() => setData([...data, { title: "New Title", author: "New Author" }]), 3000)
  // }, [])

  return (
    <AppShell header={{ height: 60, offset: false }} padding="md">
      <AppShell.Header>
        <HeaderSimple />
      </AppShell.Header>

      <AppShell.Main pt={`calc(${rem(60)} + var(--mantine-spacing-md))`}>
      <button onClick={getTime}>Time Test</button>
      <p>The current time is {currentTime}</p>
        {/* <ul>
          {data.map(d => (<li>Title: {d.title}, Author: {d.author}</li>))}
        </ul> */}
        <ul>
          {
            data.map(d =>
              ( <>
                <li>Title: {d.title}, Author: {d.author} </li>
                <ul>
                <li>GR Link: {d.link}</li>
                </ul>
                </>
              )
            )}
        </ul>
      <br></br>
      <QueryForm onFormSubmit={getBookData}></QueryForm>
      </AppShell.Main>
    </AppShell>
  );
}
