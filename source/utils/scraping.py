from typing import List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from .models import Book
import logging

DEFAULT_WAIT_SECONDS = 5
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def retrieve_goodreads_shelf_data(shelf_url: str) -> List[Book]:
    logging.info("Creating Browser")
    # Instantiate ChromeOptions
    chrome_options = webdriver.ChromeOptions()

    # Activate headless mode
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument("--incognito")
    # potentially add options.add_argument("--disable-site-isolation-trials")
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')

    # Instantiate a webdriver instance
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    book_data: List[Book] = []

    page_data = get_initial_page_soup(selenium_driver=driver, url=shelf_url)
    add_book_data_from_page(page_data_soup=page_data, book_data_list=book_data)
    next_page = page_data.select_one("a.next_page")

    while next_page is not None:
        new_page_data = get_initial_page_soup(selenium_driver=driver,
                                              url=f'https://www.goodreads.com{next_page["href"]}')
        add_book_data_from_page(page_data_soup=new_page_data, book_data_list=book_data)
        next_page = new_page_data.select_one("a.next_page")

    return book_data


def get_initial_page_soup(selenium_driver, url):
    logging.info(f"Getting Webpage Data To Parse. URL: {url}")
    selenium_driver.get(url)
    selenium_driver.implicitly_wait(DEFAULT_WAIT_SECONDS)
    return BeautifulSoup(selenium_driver.page_source, "html.parser")


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


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    # multi-page examples:
    multi_page = "https://www.goodreads.com/review/list/158747789-michael-chapman?shelf=to-read"
    # single-page example:
    single_page = "https://www.goodreads.com/review/list/158747789-michael-chapman?shelf=currently-reading"

    retrieved_book_data = retrieve_goodreads_shelf_data(multi_page)
    print(retrieved_book_data[0].isbn)
    print(len(retrieved_book_data))
