from typing import List

import requests
from bs4 import BeautifulSoup
from source.utils.models import Book
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36}'
}


def retrieve_goodreads_shelf_data(shelf_url: str) -> List[Book]:
    logging.info("Retrieving Shelf Data")

    book_data: List[Book] = []

    page_data = get_initial_page_soup(shelf_url)
    add_book_data_from_page(page_data_soup=page_data, book_data_list=book_data)
    remaining_pages = get_remaining_page_urls(page_data)

    for page in remaining_pages:
        new_page_data = get_initial_page_soup(f'https://www.goodreads.com{page}')
        add_book_data_from_page(page_data_soup=new_page_data, book_data_list=book_data)

    return book_data


def get_initial_page_soup(url):
    logging.info(f"Getting Webpage Data To Parse. URL: {url}")
    page_data = requests.get(url, headers=headers)
    return BeautifulSoup(page_data.text, "html.parser")


def get_remaining_page_urls(page_soup):
    logging.info("Parsing for remaining pages")
    if page_soup.select_one("#reviewPagination") is not None:
        return set(map(lambda x: x['href'], page_soup.select_one("#reviewPagination").select("a")))
    else:
        return []


def add_book_data_from_page(page_data_soup, book_data_list):
    logging.info(f"Parsing Book Data")
    table_rows = page_data_soup.select_one("#booksBody").select("tr")
    result = map(convert_row_to_book, table_rows)
    book_data_list.extend(list(result))


def convert_row_to_book(row_soup):
    return Book(
        title=row_soup.select_one(".title").select_one(".value").select_one("a")["title"].strip(),
        author=row_soup.select_one(".author").select_one(".value").select_one("a").getText().strip(),
        isbn=row_soup.select_one(".isbn").select_one(".value").getText().strip(),
        isbn13=row_soup.select_one(".isbn13").select_one(".value").getText().strip(),
        avg_rating=float(row_soup.select_one(".avg_rating").select_one(".value").getText().strip()),
        date_added=row_soup.select_one(".date_added").select_one(".value").getText().strip(),
        link=f'https://www.goodreads.com{row_soup.select_one(".title").select_one(".value").select_one("a")["href"]}',
    )


def get_library_availability(library_url):

    book_in_inventory = find_book_in_inventory(library_url)

    if book_in_inventory is not None:
        # Get Shelf Status
        shelf_status = book_in_inventory.parent.parent.find_all("div", {
            "class": "related-manifestation-shelf-status"
        })[0]

        if shelf_status.text.strip() == "On Shelf":
            available_sites = list(
                map(
                    lambda x: x.text.split(" - ")[0], shelf_status.parent.find_all("div", {"class": "itemSummary row"})
                )
            )
            return f"AVAILABLE: {available_sites}"

        elif shelf_status.text.strip() == "Checked Out":
            return "CHECKED OUT"
        else:
            return "UNKNOWN STATUS"
    else:
        return "Book Not Found"


def find_book_in_inventory(library_url):
    library_isbn_search = get_initial_page_soup(library_url)

    if len(library_isbn_search.find_all("a", {"aria-label": "View Book"})) > 0:
        return library_isbn_search.find_all("a", {"aria-label": "View Book"})[0]
    elif len(library_isbn_search.find_all("a", {"aria-label": "View Manifestations for Book"})) > 0:
        return library_isbn_search.find_all("a", {"aria-label": "View Manifestations for Book"})[0]
    else:
        return None


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    # multi-page examples:
    multi_page = "https://www.goodreads.com/review/list/158747789-michael-chapman?shelf=to-read"
    # single-page example:
    single_page = "https://www.goodreads.com/review/list/158747789-michael-chapman?shelf=currently-reading"

    # retrieved_book_data = retrieve_goodreads_shelf_data(multi_page)
    # print(retrieved_book_data[0].isbn)
    # print(len(retrieved_book_data))

    # get_library_availability("https://catalog.library.nashville.org/Search/Results?join=AND&lookfor0%5B%5D=9780593157534&type0%5B%5D=ISN")
    # get_library_availability("https://catalog.library.nashville.org/Search/Results?join=AND&lookfor0%5B%5D=9780441013593&type0%5B%5D=ISN")
    # get_library_availability("https://catalog.library.nashville.org/Search/Results?join=AND&lookfor0%5B%5D=9780061052651&type0%5B%5D=ISN")

