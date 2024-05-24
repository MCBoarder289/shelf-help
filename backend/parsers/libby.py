import urllib.parse
from typing import Tuple

import requests
import orjson

from libraryEnum import LibraryEnum

# Starting only with eBooks, not audiobooks or other formats (magazines)

LIBBY_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://libbyapp.com',
    'Referer': 'https://libbyapp.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}


def search_libby(library_id: LibraryEnum, title: str, author: str) -> Tuple[bool, str, str]:
    response = requests.get(
        f'https://thunder.api.overdrive.com/v2/libraries/{library_id.value}/media?query={urllib.parse.quote(title)}%20{urllib.parse.quote(author)}&format=ebook-kindle,ebook-overdrive,ebook-epub-adobe,ebook-pdf-adobe,ebook-kobo&page=1&perPage=20',
        headers=LIBBY_HEADERS,
    )

    results = orjson.loads(response.text)
    if results['items']:
        libby_item = results['items'][0]
        if libby_item['isAvailable']:
            return True, "AVAILABLE: Check link for more", f"https://libbyapp.com/search/{library_id.value}/search/query-{urllib.parse.quote(title)}%20{urllib.parse.quote(author)}/page-1/{libby_item['id']}"
        else:
            return False, "UNAVAILABLE: Check to see hold", f"https://libbyapp.com/search/{library_id.value}/search/query-{urllib.parse.quote(title)}%20{urllib.parse.quote(author)}/page-1/{libby_item['id']}"
    return False, "Item Not Found: Link to search results", f"https://libbyapp.com/search/{library_id.value}/search/query-{urllib.parse.quote(title)}%20{urllib.parse.quote(author)}/page-1/"
