import logging
import urllib.parse
from typing import List, Tuple
import random
import requests
from bs4 import BeautifulSoup

from models import USER_AGENTS

SUPPORTED_LIBRARIES = [

    {'label': 'Nashville', 'value': 'Nashville'},
    {'label': 'Miami', 'value': 'Miami'},
    {'label': 'Syracuse', 'value': 'Syracuse'},
    {'label': 'Columbus', 'value': 'Columbus'},
    {'label': 'Cincinnati', 'value': 'Cincinnati'},
    {'label': 'San Francisco', 'value': 'San Francisco'},
    {'label': 'Phoenix', 'value': 'Phoenix'},
    {'label': 'Delafield', 'value': 'Delafield'},
    {'label': 'Toledo', 'value': 'Toledo'},

]

BOOK_NOT_FOUND_MESSAGE = "Book Not Found: Check link to refine search (other locations, formats, etc.)"

# Qualities of the library parsers:
# * ISBN search
# * Free text search
# * Current focus is on Physical Books only, so filter down to those if possible?


def get_initial_page_soup(url):
    logging.info(f"Getting Webpage Data To Parse. URL: {url}")
    page_data = requests.get(url, headers={'user-agent': random.choice(USER_AGENTS)})
    return BeautifulSoup(page_data.text, "html.parser")


class BaseLibraryParser:
    """Base class for all Library Parsers"""
    def __init__(self):
        self.headers = {'user-agent': random.choice(USER_AGENTS)}

    def make_isbn_search_url(self, isbn: str) -> str:
        pass

    def make_free_text_search_url(self, title: str, author: str) -> str:
        pass

    def get_library_links(self, isbn: str, title: str, author: str) -> List[str]:
        pass

    def find_book_in_inventory(self, library_url):
        pass

    def get_library_availability(self, library_links: List[str]) -> Tuple[bool, str, str]:
        pass


class NashvillePublicLibraryParser(BaseLibraryParser):
    def __init__(self):
        super().__init__()

    def make_isbn_search_url(self, isbn) -> str:
        return f"https://catalog.library.nashville.org/Search/Results?join=AND&lookfor0%5B%5D={isbn}&type0%5B%5D=ISN"

    def make_free_text_search_url(self, title: str, author: str) -> str:
        return f"https://catalog.library.nashville.org/Union/Search?view=list&showCovers=on&lookfor={urllib.parse.quote_plus(title)}+{urllib.parse.quote_plus(author)}&searchIndex=Keyword"

    def get_library_links(self, isbn: str, title: str, author: str) -> List[str]:
        if isbn == "":
            return [
                self.make_free_text_search_url(title=title, author=author)
            ]
        else:
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

    def get_library_availability(self, library_links: List[str]) -> Tuple[bool, str, str]:
        final_availability: bool = False
        final_shelf_status: str = BOOK_NOT_FOUND_MESSAGE
        final_link: str = library_links[len(library_links)-1]
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
                    final_availability = True
                    final_shelf_status = f"AVAILABLE: {available_sites}"

                elif shelf_status.text.strip() == "Checked Out":
                    final_shelf_status = "CHECKED OUT: Check link for more details "

                else:
                    final_shelf_status = "UNKNOWN STATUS: Check link for more details"
                final_link = link
                break
            else:
                continue
        return final_availability, final_shelf_status, final_link


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

    def find_book_in_inventory(self, library_url) -> Tuple[bool, str]:
        library_isbn_search = get_initial_page_soup(library_url)
        results = library_isbn_search.find_all("span", {"class": "cp-availability-status"})
        if results:
            status = results[0].text.upper().strip()
            return status == "AVAILABLE", f"{status} - Click button to see where"
        else:
            return False, BOOK_NOT_FOUND_MESSAGE

    def get_library_availability(self, library_links: List[str]) -> Tuple[bool, str, str]:
        final_link: str = library_links[0]
        final_availability, final_shelf_status = self.find_book_in_inventory(final_link)

        return final_availability, final_shelf_status, final_link


class CincinnatiPublicLibraryParser(BaseLibraryParser):
    def __init__(self):
        super().__init__()

    def make_isbn_search_url(self, isbn: str) -> str:
        # Can't search by ISBN
        pass

    def make_free_text_search_url(self, title: str, author: str) -> str:
        return f"https://cincinnatilibrary.bibliocommons.com/v2/search?custom_edit=false&query=(title%3A({urllib.parse.quote(title)})%20AND%20contributor%3A({urllib.parse.quote(author)})%20)&searchType=bl&suppress=true&f_FORMAT=BK"

    def get_library_links(self, isbn: str, title: str, author: str) -> List[str]:
        return [
            self.make_free_text_search_url(title=title, author=author)
        ]

    def find_book_in_inventory(self, library_url) -> Tuple[bool, str]:
        library_isbn_search = get_initial_page_soup(library_url)
        results = library_isbn_search.find_all("span", {"class": "cp-availability-status"})
        if results:
            status = results[0].text.upper().strip()
            return status == "AVAILABLE", f"{status} - Click button to see where"
        else:
            return False, BOOK_NOT_FOUND_MESSAGE

    def get_library_availability(self, library_links: List[str]) -> Tuple[bool, str, str]:
        final_link: str = library_links[0]
        final_availability, final_shelf_status = self.find_book_in_inventory(final_link)

        return final_availability, final_shelf_status, final_link


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

    def find_book_in_inventory(self, library_url) -> Tuple[bool, str]:
        library_isbn_search = get_initial_page_soup(library_url)
        results = library_isbn_search.find_all("span", {"class": "cp-availability-status"})
        if results:
            status = results[0].text.upper().strip()
            return status == "AVAILABLE", f"{status} - Click button to see where"
        else:
            return False, BOOK_NOT_FOUND_MESSAGE

    def get_library_availability(self, library_links: List[str]) -> Tuple[bool, str, str]:
        final_link: str = library_links[0]
        final_availability, final_shelf_status = self.find_book_in_inventory(final_link)

        return final_availability, final_shelf_status, final_link


class MiamiPublicLibraryParser(BaseLibraryParser):
    def __init__(self):
        super().__init__()

    def make_isbn_search_url(self, isbn: str) -> str:
        # Can't search by ISBN
        pass

    def make_free_text_search_url(self, title: str, author: str) -> str:
        return f"https://mdpls.na.iiivega.com/search?query={urllib.parse.quote(title)}%20{urllib.parse.quote(author)}"

    def get_library_links(self, isbn: str, title: str, author: str) -> List[str]:
        return [
            self.make_free_text_search_url(title=title, author=author),
            f'{title} {author}'  # TODO: Hacky - make this cleaner and not index dependent
            # TODO: Add a fuzzy match title here so that we can match search results better
        ]

    def get_library_availability(self, library_links: List[str]) -> Tuple[bool, str, str]:
        final_link: str = library_links[0]
        new_headers = {'user-agent': random.choice(USER_AGENTS)}
        new_headers.update(
            {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Anonymous-User-Id': '5c645b47-9d91-4945-af3c-0db361b1cd23',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': 'https://mdpls.na.iiivega.com',
                'Referer': 'https://mdpls.na.iiivega.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'api-version': '2',
                'iii-customer-domain': 'mdpls.na.iiivega.com',
                'iii-host-domain': 'mdpls.na.iiivega.com',
                'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
            }
        )

        session = requests.Session()
        session.get(final_link, headers=new_headers)

        response = session.post(
            "https://na.iiivega.com/api/search-result/search/format-groups",
            headers=new_headers,
            json={
                'searchText': library_links[1],
                'sorting': 'relevance',
                'sortOrder': 'asc',
                'pageNum': 0,
                'pageSize': 10,  # TODO: Bring back more pages for better matches?
                'resourceType': 'FormatGroup',
            }
        )

        library_data = response.json().get("data")
        final_availability: bool = False
        final_shelf_status: str = BOOK_NOT_FOUND_MESSAGE
        if library_data:
            item_locations = [
                item['locations'] for item in library_data[0].get("materialTabs") if
                item['type'] == 'physical' and item['name'] == 'Book'
            ]
            if item_locations:
                locations = [item['label'] for item in item_locations[0] if item['availabilityStatus'] == "Available"]

                if locations:
                    final_availability = True
                    final_shelf_status = f"AVAILABLE: {locations}"
                else:
                    final_shelf_status = "UNAVAILABLE: Check search for other statuses"

        return final_availability, final_shelf_status, final_link


class SyracusePublicLibraryParser(BaseLibraryParser):
    def __init__(self):
        super().__init__()

    def make_isbn_search_url(self, isbn: str) -> str:
        return f"https://catalog.onlib.org/polaris/search/searchresults.aspx?ctx=1.1033.0.0.6&type=Keyword&term={isbn}&by=ISBN&sort=RELEVANCE&limit=(TOM=bks%20NOT%20TOM=ebk%20NOT%20TOM=elr%20NOT%20TOM=abk)%20AND%20AB=*&query=&page=0"

    def make_free_text_search_url(self, title: str, author: str) -> str:  # TODO: Cleanup URL encoding for the title (since we include quotes now)
        return f'https://catalog.onlib.org/polaris/search/searchresults.aspx?ctx=1.1033.0.0.6&type=Keyword&term=%22{urllib.parse.quote(title)}%22%20%22{urllib.parse.quote(author)}%22&by=KW&sort=RELEVANCE&limit=(TOM=bks%20NOT%20TOM=ebk%20NOT%20TOM=elr%20NOT%20TOM=abk)%20AND%20AB=*&query=&page=0'

    def get_library_links(self, isbn: str, title: str, author: str) -> List[str]:
        return [
            self.make_isbn_search_url(isbn=isbn),
            self.make_free_text_search_url(title=title, author=author)
        ]

    def find_book_in_inventory(self, library_url):
        session = requests.Session()
        headers = {'user-agent': random.choice(USER_AGENTS)}
        session.get(library_url, headers=headers)
        new_headers = headers.copy()
        new_headers.update(
            {
                "Referer": library_url,
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "Connection": "keep-alive",
                "X-Requested-With": "XMLHttpRequest",
            }
        )
        response = session.get(
            "https://catalog.onlib.org/polaris/search/components/ajaxResults.aspx?page=1",
            headers=new_headers,
            params={"page": 1},
        )

        inventory_check = (None, None)

        if response.ok:
            inventory_soup = BeautifulSoup(response.text, "html.parser")
            local_availability = inventory_soup.find_all("span", "nsm-brief-inline-subzone")
            if local_availability:
                all_copies = local_availability[0].text.replace("(", "").replace("of", "").replace(")", "").split()
                avail_copies = int(all_copies[0])
                total_copies = int(all_copies[1])
                if avail_copies != 0:
                    inventory_check = (f"AVAILABLE: {avail_copies} copies are local out of {total_copies} total copies. Check Link to see locations.", library_url)
                else:
                    inventory_check = (f"UNAVAILABLE: {avail_copies} copies are local out of {total_copies} total copies. Check Link to see locations.", library_url)

        return inventory_check

    def get_library_availability(self, library_links: List[str]) -> Tuple[bool, str, str]:
        final_shelf_status: str = BOOK_NOT_FOUND_MESSAGE
        final_link: str = library_links[1]
        final_availability: bool = False
        for link in library_links:
            status, url = self.find_book_in_inventory(link)

            if status is not None and status.startswith("AVAILABLE"):
                final_availability = True
                final_shelf_status = status
                final_link = url
                break
            elif status is not None and status.startswith("UNAVAILABLE"):
                final_shelf_status = status
                final_link = url

        return final_availability, final_shelf_status, final_link


class PhoenixPublicLibraryParser(BaseLibraryParser):
    def __init__(self):
        super().__init__()

    def make_isbn_search_url(self, isbn: str) -> str:
        return f"https://catalog.phoenixpubliclibrary.org/search/searchresults.aspx?ctx=1.1033.0.0.35&type=Advanced&term={isbn}&relation=ALL&by=ISBN&bool4=AND&limit=MAT=1&sort=RELEVANCE&page=0"

    def make_free_text_search_url(self, title: str, author: str) -> str:
        return f'https://catalog.phoenixpubliclibrary.org/search/searchresults.aspx?ctx=1.1033.0.0.35&type=Advanced&term={title}&relation=ALL&by=TI&term2={urllib.parse.quote(author)}&relation2=ALL&by2=AU&bool1=AND&bool4=AND&limit=MAT=1&sort=RELEVANCE&page=0'

    def get_library_links(self, isbn: str, title: str, author: str) -> List[str]:
        return [
            self.make_isbn_search_url(isbn=isbn),
            self.make_free_text_search_url(title=title, author=author)
        ]

    def find_book_in_inventory(self, library_url):
        session = requests.Session()
        headers = {'user-agent': random.choice(USER_AGENTS)}
        session.get(library_url, headers=headers)
        new_headers = headers.copy()
        new_headers.update(
            {
                "Referer": library_url,
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "Connection": "keep-alive",
                "X-Requested-With": "XMLHttpRequest",
            }
        )
        response = session.get(
            "https://catalog.phoenixpubliclibrary.org/search/components/ajaxResults.aspx",
            headers=new_headers,
            params={"page": 1},
        )

        inventory_check = (None, None)

        if response.ok:
            inventory_soup = BeautifulSoup(response.text, "html.parser")
            local_availability = inventory_soup.find_all("span", "nsm-brief-inline-subzone")
            if local_availability:
                all_copies = local_availability[0].text.replace("(", "").replace("of", "").replace(")", "").split()
                avail_copies = int(all_copies[0])
                total_copies = int(all_copies[1])
                if avail_copies != 0:
                    inventory_check = (f"AVAILABLE: {avail_copies} copies are local out of {total_copies} total copies. Check Link to see locations.", library_url)
                else:
                    inventory_check = (f"UNAVAILABLE: {avail_copies} copies are local out of {total_copies} total copies. Check Link to see locations.", library_url)

        return inventory_check

    def get_library_availability(self, library_links: List[str]) -> Tuple[bool, str, str]:
        final_shelf_status: str = BOOK_NOT_FOUND_MESSAGE
        final_link: str = library_links[1]
        final_availability: bool = False
        for link in library_links:
            status, url = self.find_book_in_inventory(link)

            if status is not None and status.startswith("AVAILABLE"):
                final_availability = True
                final_shelf_status = status
                final_link = url
                break
            elif status is not None and status.startswith("UNAVAILABLE"):
                final_shelf_status = status
                final_link = url

        return final_availability, final_shelf_status, final_link


class DelafieldPublicLibraryParser(BaseLibraryParser):
    def __init__(self):
        super().__init__()

    def make_isbn_search_url(self, isbn: str) -> str:
        return f"https://www.cafelibraries.org/polaris/search/searchresults.aspx?ctx=6.1033.0.0.5&type=Keyword&term={isbn}&by=ISBN&sort=RELEVANCE&limit=TOM=bks&query=&page=0"

    def make_free_text_search_url(self, title: str, author: str) -> str:
        return f'https://www.cafelibraries.org/polaris/search/searchresults.aspx?ctx=6.1033.0.0.5&type=Keyword&term={title}%20{urllib.parse.quote(author)}&by=KW&sort=RELEVANCE&limit=TOM=bks&query=&page=0'

    def get_library_links(self, isbn: str, title: str, author: str) -> List[str]:
        return [
            self.make_isbn_search_url(isbn=isbn),
            self.make_free_text_search_url(title=title, author=author)
        ]

    def find_book_in_inventory(self, library_url):
        session = requests.Session()
        headers = {'user-agent': random.choice(USER_AGENTS)}
        session.get(library_url, headers=headers)
        new_headers = headers.copy()
        new_headers.update(
            {
                "Referer": library_url,
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "Connection": "keep-alive",
                "X-Requested-With": "XMLHttpRequest",
            }
        )
        response = session.get(
            "https://www.cafelibraries.org/polaris/search/components/ajaxResults.aspx?page=1",
            headers=new_headers,
            params={"page": 1},
        )

        inventory_check = (None, None)

        if response.ok:
            inventory_soup = BeautifulSoup(response.text, "html.parser")

            # Filtering out overdrive and Large Print Editions, since they come up at the top of searches
            non_overdrive_books = [item for item in inventory_soup.find_all("span", "nsm-short-item nsm-e105") if not "OverDrive" in item.text and not "Large print" in item.text]

            if non_overdrive_books:
                local_availability = non_overdrive_books[0].findParents("table")[0].find_all_next("span", "nsm-brief-inline-subzone")
            else:
                local_availability = None

            if local_availability:
                local_avail_copies, local_total_copies = self.get_available_copies(local_availability[0])
                avail_copies, total_copies = self.get_available_copies(local_availability[1])

                if local_total_copies != 0:
                    inventory_check = (f"AVAILABLE - Locally: {local_avail_copies} out of {local_total_copies} at THIS library, {avail_copies} out of {total_copies} at ALL libraries", library_url)
                elif avail_copies != 0:
                    inventory_check = (f"AVAILABLE - Other Libraries: {local_avail_copies} out of {local_total_copies} at THIS library, {avail_copies} out of {total_copies} at ALL libraries", library_url)
                else:
                    inventory_check = (f"UNAVAILABLE: {local_avail_copies} out of {local_total_copies} at THIS library, {avail_copies} out of {total_copies} at ALL libraries", library_url)

        return inventory_check

    def get_available_copies(self, local_availability_item):
        all_copies = local_availability_item.text.replace("(", "").replace("of", "").replace(")", "").split()
        avail_copies = int(all_copies[0])
        total_copies = int(all_copies[1])
        return avail_copies, total_copies

    def get_library_availability(self, library_links: List[str]) -> Tuple[bool, str, str]:
        final_shelf_status: str = BOOK_NOT_FOUND_MESSAGE
        final_link: str = library_links[1]
        final_availability: bool = False
        for link in library_links:
            status, url = self.find_book_in_inventory(link)

            if status is not None and status.startswith("AVAILABLE"):
                final_availability = True
                final_shelf_status = status
                final_link = url
                break
            elif status is not None and status.startswith("UNAVAILABLE"):
                final_shelf_status = status
                final_link = url

        return final_availability, final_shelf_status, final_link


class ToledoPublicLibraryParser(BaseLibraryParser):
    def __init__(self):
        super().__init__()

    def make_isbn_search_url(self, isbn: str) -> str:
        # Can't search by ISBN
        pass

    def make_free_text_search_url(self, title: str, author: str) -> str:
        return f"https://toledo.bibliocommons.com/v2/search?custom_edit=false&query=(title%3A({urllib.parse.quote(title)})%20AND%20contributor%3A({urllib.parse.quote(author)})%20)&searchType=bl&suppress=true&f_FORMAT=BK"

    def get_library_links(self, isbn: str, title: str, author: str) -> List[str]:
        return [
            self.make_free_text_search_url(title=title, author=author)
        ]

    def find_book_in_inventory(self, library_url) -> Tuple[bool, str]:
        library_isbn_search = get_initial_page_soup(library_url)
        results = library_isbn_search.find_all("span", {"class": "cp-availability-status"})
        if results:
            status = results[0].text.upper().strip()
            return status == "AVAILABLE", f"{status} - Click button to see where"
        else:
            return False, BOOK_NOT_FOUND_MESSAGE

    def get_library_availability(self, library_links: List[str]) -> Tuple[bool, str, str]:
        final_link: str = library_links[0]
        final_availability, final_shelf_status = self.find_book_in_inventory(final_link)

        return final_availability, final_shelf_status, final_link


def parser_factory(library_name="Nashville") -> BaseLibraryParser:
    """Factory Method for returning correct library parser"""
    # See
    library_parsers = {
        "nashville": NashvillePublicLibraryParser,
        "mdpls": MiamiPublicLibraryParser,
        "onlib": SyracusePublicLibraryParser,
        "clc": ColumbusPublicLibraryParser,
        "sfpl": SanFranPublicLibraryParser,
        "cincinnatilibrary": CincinnatiPublicLibraryParser,
        "phoenix": PhoenixPublicLibraryParser,
        "wplc": DelafieldPublicLibraryParser,
        "toledo": ToledoPublicLibraryParser,
    }

    return library_parsers[library_name]()


if __name__ == "__main__":
    # TODO: Make Actual Tests for this
    n = parser_factory("Nashville")
    m = parser_factory("Columbus")
