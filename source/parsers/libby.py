import urllib.parse
from typing import Tuple

import requests
import orjson

# TODO: Make this not hard coded and allow for library searches
# Took the id/preferred key for each from:
# https://thunder.api.overdrive.com/v2/libraries/?websiteIds=239,94
#
# [
#     {'label': 'Nashville', 'value': '239'},
#     {'label': 'Miami', 'value': '94'},
#     {'label': 'Syracuse', 'value': '122'},
#     {'label': 'Columbus', 'value': '49'},
#     {'label': 'Cincinnati', 'value': '47'},
#     {'label': 'San Francisco', 'value': '372'},
#     {'label': 'Phoenix', 'value': '34'},
#     {'label': 'Delafield', 'value': '80'},
#     {'label': 'Toledo', 'value': '64'},
# ]

LIBBY_LIBRARIES = [
    {'label': 'Nashville', 'value': 'nashville'},
    {'label': 'Miami', 'value': 'mdpls'},
    {'label': 'Syracuse', 'value': 'onlib'},
    {'label': 'Columbus', 'value': 'clc'},
    {'label': 'Cincinnati', 'value': 'cincinnatilibrary'},
    {'label': 'San Francisco', 'value': 'sfpl'},
    {'label': 'Phoenix', 'value': 'phoenix'},
    {'label': 'Delafield', 'value': 'wplc'},
    {'label': 'Toledo', 'value': 'toledo'},
]

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


def search_libby(library_id: str, title: str, author: str) -> Tuple[str, str]:
    response = requests.get(
        f'https://thunder.api.overdrive.com/v2/libraries/{library_id}/media?query={urllib.parse.quote(title)}%20{urllib.parse.quote(author)}&format=ebook-kindle,ebook-overdrive,ebook-epub-adobe,ebook-pdf-adobe,ebook-kobo&page=1&perPage=20',
        headers=LIBBY_HEADERS,
    )

    results = orjson.loads(response.text)
    if results['items']:
        libby_item = results['items'][0]
        if libby_item['isAvailable']:
            return "AVAILABLE: Check link for more", f"https://libbyapp.com/search/{library_id}/search/query-{urllib.parse.quote(title)}%20{urllib.parse.quote(author)}/page-1/{libby_item['id']}"
        else:
            return "UNAVAILABLE: Check to see hold", f"https://libbyapp.com/search/{library_id}/search/query-{urllib.parse.quote(title)}%20{urllib.parse.quote(author)}/page-1/{libby_item['id']}"
    return "Item Not Found: Link to search results", f"https://libbyapp.com/search/{library_id}/search/query-{urllib.parse.quote(title)}%20{urllib.parse.quote(author)}/page-1/"
