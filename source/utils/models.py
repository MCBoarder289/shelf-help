from dataclasses import dataclass
from typing import List

MAX_PAGES = 10  # If List of Pages is so big, then randomly reduce it down to this number


@dataclass
class Book:
    """DataClass for holding book information"""
    title: str
    author: str
    isbn: str
    isbn13: str
    avg_rating: float
    date_added: str
    link: str
    library_links: List[str]

