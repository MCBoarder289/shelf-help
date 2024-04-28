import logging
import urllib.parse
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from source.utils.models import HEADERS

SUPPORTED_LIBRARIES = [
    "Nashville",
    "Columbus",
    "San Francisco"
]


def get_initial_page_soup(url):
    logging.info(f"Getting Webpage Data To Parse. URL: {url}")
    page_data = requests.get(url, headers=HEADERS)
    return BeautifulSoup(page_data.text, "html.parser")


class BaseLibraryParser:
    """Base class for all Library Parsers"""
    def __init__(self):
        self.headers = HEADERS

    def make_isbn_search_url(self, isbn: str) -> str:
        pass

    def make_free_text_search_url(self, title: str, author: str) -> str:
        pass

    def get_library_links(self, isbn: str, title: str, author: str) -> List[str]:
        pass

    def find_book_in_inventory(self, library_url):
        pass

    def get_library_availability(self, library_links: List[str]) -> Tuple[str, str]:
        pass


class NashvillePublicLibraryParser(BaseLibraryParser):
    def __init__(self):
        super().__init__()

    def make_isbn_search_url(self, isbn) -> str:
        return f"https://catalog.library.nashville.org/Search/Results?join=AND&lookfor0%5B%5D={isbn}&type0%5B%5D=ISN"

    def make_free_text_search_url(self, title: str, author: str) -> str:
        return f"https://catalog.library.nashville.org/Union/Search?view=list&showCovers=on&lookfor={urllib.parse.quote_plus(title)}+{urllib.parse.quote_plus(author)}&searchIndex=Keyword"

    def get_library_links(self, isbn: str, title: str, author: str) -> List[str]:
        return [
            self.make_isbn_search_url(isbn=isbn),
            self.make_free_text_search_url(title=title, author=author)
        ]

    def find_book_in_inventory(self, library_url):
        library_isbn_search = get_initial_page_soup(library_url)

        if len(library_isbn_search.find_all("a", {"aria-label": "View Book"})) > 0:
            return library_isbn_search.find_all("a", {"aria-label": "View Book"})[0]
        elif len(library_isbn_search.find_all("a", {"aria-label": "View Manifestations for Book"})) > 0:
            return library_isbn_search.find_all("a", {"aria-label": "View Manifestations for Book"})[0]
        else:
            return None

    def get_library_availability(self, library_links: List[str]) -> Tuple[str, str]:
        final_shelf_status: str = "Book Not Found"
        final_link: str = library_links[1]  #
        for link in library_links:
            book_in_inventory = self.find_book_in_inventory(link)

            if book_in_inventory is not None:
                # Get Shelf Status
                shelf_status = book_in_inventory.parent.parent.find_all("div", {
                    "class": "related-manifestation-shelf-status"
                })[0]

                if shelf_status.text.strip() == "On Shelf":
                    available_sites = list(
                        map(
                            lambda x: x.text.split(" - ")[0],
                            shelf_status.parent.find_all("div", {"class": "itemSummary row"})
                        )
                    )
                    final_shelf_status = f"AVAILABLE: {available_sites}"

                elif shelf_status.text.strip() == "Checked Out":
                    final_shelf_status = "CHECKED OUT"

                else:
                    final_shelf_status = "UNKNOWN STATUS"
                final_link = link
                break
            else:
                continue
        return final_shelf_status, final_link


class ColumbusPublicLibraryParser(BaseLibraryParser):
    def __init__(self):
        super().__init__()

    def make_isbn_search_url(self, isbn: str) -> str:
        # Can't search by ISBN
        pass

    def make_free_text_search_url(self, title: str, author: str) -> str:
        return f"https://cml.bibliocommons.com/v2/search?custom_edit=false&query=(title%3A({urllib.parse.quote(title)})%20AND%20contributor%3A({urllib.parse.quote(author)})%20)&searchType=bl&suppress=true&f_FORMAT=BK"

    def get_library_links(self, isbn: str, title: str, author: str) -> List[str]:
        return [
            self.make_free_text_search_url(title=title, author=author)
        ]

    def find_book_in_inventory(self, library_url):
        library_isbn_search = get_initial_page_soup(library_url)
        results = library_isbn_search.find_all("span", {"class": "cp-availability-status"})
        if results:
            return f"{results[0].text.upper()} - Click button to see where"
        else:
            return None

    def get_library_availability(self, library_links: List[str]) -> Tuple[str, str]:
        # TODO: Actually Implement Another Library
        final_shelf_status: str = "Book Not Found"
        final_link: str = library_links[0]
        book_in_inventory = self.find_book_in_inventory(final_link)
        if book_in_inventory is not None:
            final_shelf_status = book_in_inventory

        return final_shelf_status, final_link


class SanFranPublicLibraryParser(BaseLibraryParser):
    def __init__(self):
        super().__init__()

    def make_isbn_search_url(self, isbn: str) -> str:
        # Can't search by ISBN
        pass

    def make_free_text_search_url(self, title: str, author: str) -> str:
        return f"https://sfpl.bibliocommons.com/v2/search?custom_edit=false&query=(title%3A({urllib.parse.quote(title)})%20AND%20contributor%3A({urllib.parse.quote(author)})%20)&searchType=bl&suppress=true&f_FORMAT=BK"

    def get_library_links(self, isbn: str, title: str, author: str) -> List[str]:
        return [
            self.make_free_text_search_url(title=title, author=author)
        ]

    def find_book_in_inventory(self, library_url):
        library_isbn_search = get_initial_page_soup(library_url)
        results = library_isbn_search.find_all("span", {"class": "cp-availability-status"})
        if results:
            return f"{results[0].text.upper()} - Click button to see where"
        else:
            return None

    def get_library_availability(self, library_links: List[str]) -> Tuple[str, str]:
        # TODO: Actually Implement Another Library
        final_shelf_status: str = "Book Not Found"
        final_link: str = library_links[0]
        book_in_inventory = self.find_book_in_inventory(final_link)
        if book_in_inventory is not None:
            final_shelf_status = book_in_inventory

        return final_shelf_status, final_link


def parser_factory(library_name="Nashville") -> BaseLibraryParser:
    """Factory Method for returning correct library parser"""
    library_parsers = {
        "Nashville": NashvillePublicLibraryParser,
        "Columbus": ColumbusPublicLibraryParser,
        "San Francisco": SanFranPublicLibraryParser,
    }

    return library_parsers[library_name]()


if __name__ == "__main__":
    # TODO: Make Actual Tests for this
    n = parser_factory("Nashville")
    m = parser_factory("Columbus")
