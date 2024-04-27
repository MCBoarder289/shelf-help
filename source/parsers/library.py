import logging
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from source.utils.models import HEADERS

SUPPORTED_LIBRARIES = ["Nashville"]


class BaseLibraryParser:
    """Base class for all Library Parsers"""
    def __init__(self):
        self.headers = HEADERS

    def get_initial_page_soup(self, url):
        logging.info(f"Getting Webpage Data To Parse. URL: {url}")
        page_data = requests.get(url, headers=self.headers)
        return BeautifulSoup(page_data.text, "html.parser")

    def get_library_availability(self, library_links: List[str]) -> Tuple[str, str]:
        pass


class NashvillePublicLibraryParser(BaseLibraryParser):
    def __init__(self):
        super().__init__()

    def find_book_in_inventory(self, library_url):
        library_isbn_search = super().get_initial_page_soup(library_url)

        if len(library_isbn_search.find_all("a", {"aria-label": "View Book"})) > 0:
            return library_isbn_search.find_all("a", {"aria-label": "View Book"})[0]
        elif len(library_isbn_search.find_all("a", {"aria-label": "View Manifestations for Book"})) > 0:
            return library_isbn_search.find_all("a", {"aria-label": "View Manifestations for Book"})[0]
        else:
            return None

    def get_library_availability(self, library_links: List[str]) -> Tuple[str, str]:
        final_shelf_status: str = "Book Not Found"
        final_link: str = library_links[1]
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


class MiamiPublicLibraryParser(BaseLibraryParser):
    def __init__(self):
        super().__init__()

    def get_library_availability(self, library_links: List[str]) -> Tuple[str, str]:
        # TODO: Actually Implement Another Library
        return "TODO", "https://www.google.com"


def parser_factory(library_name="Nashville"):
    """Factory Method for returning correct library parser"""
    library_parsers = {
        "Nashville": NashvillePublicLibraryParser,
        "Miami": MiamiPublicLibraryParser,
    }

    return library_parsers[library_name]()


if __name__ == "__main__":
    # TODO: Make Actual Tests for this
    n = parser_factory("Nashville")
    m = parser_factory("Miami")

    library_results = ['https://catalog.library.nashville.org/Search/Results?join=AND&lookfor0%5B%5D=044900483X&type0%5B%5D=ISN', 'https://catalog.library.nashville.org/Union/Search?view=list&showCovers=on&lookfor=Children+of+God+Russell%2C+Mary+Doria&searchIndex=Keyword']

    print(n.get_library_availability(library_results))
    print(m.get_library_availability(library_results))
