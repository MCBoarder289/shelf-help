
from pydantic import BaseModel, ConfigDict
from typing import List
from libraryEnum import LibraryEnum

MAX_PAGES = 10  # If List of Pages is so big, then randomly reduce it down to this number

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36}'
}

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36}'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]


class Book(BaseModel):
    """DataClass for holding book information"""
    title: str
    author: str
    isbn: str
    avg_rating: float
    date_added: str
    link: str
    searchable_title: str
    image_link: str
    goodreads_id: str


class BookList(BaseModel):
    books: List[Book]


class GetBooksRequest(BaseModel):
    num_books: int
    gr_url: str

    model_config = ConfigDict(extra='forbid')


class LibraryStatusRequest(BaseModel):
    is_libby: bool
    library: LibraryEnum
    book: Book

    model_config = ConfigDict(extra='forbid')


class LibraryStatusResponse(BaseModel):
    is_available: bool
    msg: str
    link: str

