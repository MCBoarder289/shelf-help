from typing import List, Tuple

import re
import requests
import random
from bs4 import BeautifulSoup

from source.parsers.library import get_initial_page_soup, parser_factory
from source.utils.models import Book, MAX_PAGES, HEADERS
import urllib.parse
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def retrieve_goodreads_shelf_data(shelf_url: str) -> List[Book]:
    logging.info("Retrieving Shelf Data")
    book_data: List[Book] = []

    pages = retrieve_goodreads_page_list(shelf_url)

    for page in pages:
        new_page_data = get_initial_page_soup(page)
        add_book_data_from_page(page_data_soup=new_page_data, book_data_list=book_data)

    return book_data


def retrieve_goodreads_page_list(shelf_url: str) -> List[str]:
    logging.info("Retrieving List of Goodreads Pages")
    page_list: List[str] = []
    page_data = get_initial_page_soup(shelf_url)
    remaining_pages = get_remaining_page_urls(page_data)
    page_list.append(shelf_url)
    page_list.extend(remaining_pages)
    return page_list


def get_remaining_page_urls(page_soup):
    logging.info("Parsing for remaining pages")
    if page_soup.select_one("#reviewPagination") is not None:
        present_links = list(map(lambda x: f"https://www.goodreads.com{x['href']}", page_soup.select_one("#reviewPagination").select("a")))
        max_page = max([int(re.search(r"(?<=page=)\d+", url).group()) for url in present_links])
        if max_page < MAX_PAGES:
            return [re.sub(r"(?<=page=)\d+", str(i), present_links[0]) for i in range(2, max_page + 1)]
        else:
            return [re.sub(r"(?<=page=)\d+", str(i), present_links[0]) for i in random.sample(range(2, max_page), MAX_PAGES)]
    else:
        return []


def add_book_data_from_page(page_data_soup, book_data_list):
    logging.info(f"Parsing Book Data")
    table_rows = page_data_soup.select_one("#booksBody").select("tr")
    result = map(convert_row_to_book, table_rows)
    book_data_list.extend(list(result))


def convert_row_to_book(row_soup):
    title = row_soup.select_one(".title").select_one(".value").select_one("a")["title"].strip()
    searchable_title = title.partition("(")[0].strip() if "(" in title else title
    author = row_soup.select_one(".author").select_one(".value").select_one("a").getText().strip()
    isbn = get_isbn(row_soup, title=searchable_title, author=author)
    return Book(
        title=title,
        author=author,
        isbn=isbn,
        isbn13=row_soup.select_one(".isbn13").select_one(".value").getText().strip(),
        avg_rating=float(row_soup.select_one(".avg_rating").select_one(".value").getText().strip()),
        date_added=row_soup.select_one(".date_added").select_one(".value").getText().strip(),
        link=f'https://www.goodreads.com{row_soup.select_one(".title").select_one(".value").select_one("a")["href"]}',
        searchable_title=searchable_title,
    )


def get_isbn(row_soup, title, author):
    parsed_isbn = row_soup.select_one(".isbn").select_one(".value").getText().strip()
    if parsed_isbn != "":
        return parsed_isbn
    else:
        logging.info("ISBN Not Found... Attempting to Discover")
        isbn = ""
        query_response = requests.get(
            f"https://openlibrary.org/search.json?q=title:{urllib.parse.quote_plus(title.lower())}+author:{urllib.parse.quote_plus(author.lower())}",
            headers=HEADERS
        )
        if query_response.ok:
            response_json = query_response.json()
            if response_json["num_found"] > 0:
                isbn_list = response_json["docs"][0].get("isbn", [])
                if isbn_list:
                    isbn = isbn_list[0]

        return isbn


if __name__ == "__main__":
    # TODO: Refactor these into actual tests
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    # multi-page examples:
    multi_page = "https://www.goodreads.com/review/list/158747789-michael-chapman?shelf=to-read"
    many_page = "https://www.goodreads.com/review/list/73257606-cole?ref=nav_mybooks&shelf=to-read"
    # single-page example:
    single_page = "https://www.goodreads.com/review/list/158747789-michael-chapman?shelf=currently-reading"

    # page_list = retrieve_goodreads_page_list(many_page)

    retrieved_book_data = retrieve_goodreads_shelf_data(many_page)
    print(retrieved_book_data[0].isbn)
    print(len(retrieved_book_data))