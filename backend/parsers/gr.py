import time
from typing import List, Optional

import requests
import orjson

import random
from parsers.library import get_initial_page_soup
from models import Book, HEADERS, BookDict, USER_AGENTS
from lxml import etree
import urllib.parse
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

PER_PAGE_MAX = 200
TOTAL_BOOKS_MAX = 800


def retrieve_goodreads_shelf_data(shelf_url: str) -> BookDict:
    logging.info("Retrieving Shelf Data")
    rss_link = get_rss_link(shelf_url)
    return retrieve_books_from_rss_feeds(rss_link)


def get_rss_link(shelf_url: str, retries: int = 5, backoff_factor: int = 2) -> Optional[str]:
    attempt = 0
    while attempt < retries:
        try:
            soup = get_initial_page_soup(shelf_url)
            error = soup.find("div", {"class": "errorBox"})
            if error:
                if "private" in error.text.strip().lower():
                    raise RuntimeError("The shelf you are trying to reference is private. Update your Goodreads profile to be public in order to use Shelf Help.")
                else:
                    raise RuntimeError(f"We are getting an unexpected error from Goodreads: {error.text.strip()}")
            element = soup.find("link", attrs={"rel": "alternate"})
            if element and element.get("href"):
                return element["href"]
            else:
                raise ValueError("Failed to find a valid RSS link")
        except (requests.RequestException, ValueError) as e:
            # Exponential Backoff
            attempt += 1
            wait_time = backoff_factor ** attempt
            logging.info(f"Attempt {attempt} failed: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    logging.error(f"Failed to retrieve RSS link after {retries} attempts.")
    return None


def fetch_rss_feed(url: str) -> bytes:
    response = requests.get(url, headers={'user-agent': random.choice(USER_AGENTS)})
    return response.content


def parse_rss(feed_content: bytes):
    root = etree.fromstring(feed_content)
    items = root.findall(".//item")

    return items


def retrieve_books_from_rss_feeds(rss_url: str, max_items: int = TOTAL_BOOKS_MAX):
    page = 1
    not_complete = True
    book_data_list: List[Book] = []
    while not_complete:
        feed_content = fetch_rss_feed(f"{rss_url}&page={page}&per_page={PER_PAGE_MAX}")
        results = parse_rss(feed_content)
        if len(results) == 0 or len(results) + len(book_data_list) >= max_items:
            not_complete = False
        else:
            book_data_list.extend(list(map(convert_rss_item_to_book, results)))
            page += 1
    return BookDict(books={f"{book.searchable_title} - {book.author}": book for book in book_data_list})


def convert_rss_item_to_book(rss_item) -> Book:
    title = rss_item.findtext("title")
    searchable_title = title.partition("(")[0].strip() if "(" in title else title
    author = ' '.join(rss_item.findtext("author_name").split())  # TODO: See if this is ok vs. lastname, first
    isbn = get_isbn(rss_item.findtext("isbn"), title, author)
    return Book(
        title=title,
        author=author,
        isbn=isbn,
        avg_rating=float(rss_item.findtext("average_rating")),
        date_added=rss_item.findtext("user_date_added"),
        link=f"https://www.goodreads.com/book/show/{rss_item.findtext("book_id")}",
        searchable_title=searchable_title,
        image_link=rss_item.findtext("book_large_image_url"),
        goodreads_id=rss_item.findtext("book_id"),
    )


def get_isbn(isbn, title, author, skip_isbn_check=True):
    if isbn != "" or skip_isbn_check:
        return isbn
    else:
        logging.info("ISBN Not Found... Attempting to Discover")
        new_isbn = ""
        query_response = requests.get(
            f"https://openlibrary.org/search.json?q=title:{urllib.parse.quote_plus(title.lower())}+author:{urllib.parse.quote_plus(author.lower())}",
            headers=HEADERS
        )
        if query_response.ok:
            response_json = orjson.loads(query_response.text)
            if response_json["num_found"] > 0:
                isbn_list = response_json["docs"][0].get("isbn", [])
                if isbn_list:
                    new_isbn = isbn_list[0]

        return new_isbn


if __name__ == "__main__":
    # TODO: Refactor these into actual tests
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    # multi-page examples:
    multi_page = "https://www.goodreads.com/review/list/158747789-michael-chapman?shelf=to-read"
    many_page = "https://www.goodreads.com/review/list/73257606-cole?ref=nav_mybooks&shelf=to-read"
    # single-page example:
    single_page = "https://www.goodreads.com/review/list/158747789-michael-chapman?shelf=currently-reading"

    # page_list = retrieve_goodreads_page_list(many_page)
    start = time.time()

    retrieved_book_data = retrieve_goodreads_shelf_data(many_page)

    end = time.time()

    print(end - start)
    # from operator import itemgetter
    # import random
    # import timeit
    #
    # book_dict = {f"{book.title} - {book.author}": book for book in retrieved_book_data}
    # book_keys = random.sample(sorted(book_dict.keys()), 100)
    # code = "results = list(itemgetter(*book_keys)(book_dict))"
    #
    # item_getter_results = timeit.repeat(stmt=code, number=1000, setup="from operator import itemgetter", globals=globals())
    # list_comp_results = timeit.repeat(stmt="""results = [book_dict[book] for book in book_keys]""", number=1000, globals=globals())
    print(retrieved_book_data[0].isbn)
    print(len(retrieved_book_data))
